import csv
import logging
from datetime import datetime
from operator import attrgetter, itemgetter
from pathlib import Path

import pandas as pd
import pdfkit
import simplejson as json
from flask import Response, request, jsonify, render_template, make_response, send_file, url_for
from flask import current_app
from flask_mail import Message
from flask_restful import Resource
from werkzeug.exceptions import HTTPException

from app import db, mail
from app.blueprints.case_management import helper_dr486_pdf_template
from app.case_management.lookup import EntityName
from app.case_management.mixins import StateChangedMixin
from app.case_management.models import Application, ApplicationSchema, Client, ClientSchema, \
    CaseProperty, CasePropertySchema, NoteSchema, Tag, \
    TagSchema, ClientType, ApplicationType, ApplicationTypeSchema, MarketingCode, \
    MarketingCodeSchema, Note, NoteSender, ApplicationStatus, NoteType, RejectReason, \
    RejectReasonSchema, PaymentType, PaymentTypeSchema, ApplicationStatusSchema, ClientTypeSchema, Takeover, \
    TakeoverSchema, ApplicationSource, ApplicationSourceSchema, PaymentStatus, PaymentStatusSchema, \
    CaseEmail, EmailOriginator, NoteDescription, SenderNoteSchema
from app.case_management.services import CaseService, EmailService, EvidenceService
from app.database.models import Owner, Assessment, Property
from app.database.models.user import Permission
from app.email import EmailToClient, send_email, make_and_send_email
from app.pdf.sign_pdf import prepare_pdf_attachment, encode_latin1_to_utf8
from app.routing.decorators import permission_required, domains_allowed, Domain
from app.routing.errors import bad_request, not_found, server_error, ServerError, NotFoundError
from app.routing.services import PropertyService, PetitionsReportService
from app.settings.models import AssessmentDate
from app.singlecma.models import SingleCMAWorkupsSchema, SingleCMAWorkups
from app.utils.constants import County
from app.utils.fix_address import capitalize_address
from config import DATA_IMPORT
from my_logger import logger


class DomainResource(Resource):
    method_decorators = [domains_allowed(Domain.BETA, Domain.REDUX, Domain.BETA_REDUX)]


class TakeoversApi(DomainResource):
    def get(self, application_id=None):
        """
        Get all takeovers or get all application takeovers
        """
        if application_id:
            query = Takeover.query.filter_by(application_id=application_id)
        else:
            query = Takeover.query

        takeovers = query.all()
        return jsonify(TakeoverSchema().dump(takeovers, many=True))

    def post(self):
        data = request.get_json()
        errors = TakeoverSchema().validate(data)

        # respond validation errors
        if errors:
            return bad_request(errors)

        takeover = TakeoverSchema(exclude=('id',)).load(data)
        takeover.save()

        return jsonify(TakeoverSchema().dump(takeover))


class TakeoverApi(DomainResource):
    def get(self, takeover_id):
        """
        Get specific takeover
        """
        takeover = Takeover.get(takeover_id)
        return jsonify(TakeoverSchema().dump(takeover))

    def delete(self, takeover_id):
        """
        Delete specific takeover
        """
        try:
            takeover = Takeover.get_or_404(takeover_id)
            takeover.delete()
            return jsonify({'status': True})
        except HTTPException:
            response = jsonify(error="Takeover with id={} was not found".format(takeover_id))
            response.status_code = 404
            return response


class LookupApi(DomainResource):

    def post(self, entity_name):
        data = request.get_json()

        if entity_name == EntityName.CLIENT:
            clients = CaseService.get_lookup_clients(data['filters'])
            return jsonify(ClientSchema(exclude=('applications',)).dump(clients, many=True))

        elif entity_name == EntityName.CASE:
            cases = CaseService.get_lookup_cases(data['filters'])
            return jsonify(CasePropertySchema(exclude=('application', )).dump(cases, many=True))

        else:
            return bad_request(message=f"Invalid entity name: {entity_name}")


class LookupReportApi(DomainResource):
    REPORT_COLUMNS = ['Folio', 'Address', 'Client name', 'Assessment value']

    def post(self, entity_name):
        """
        Export lookup results .csv file
        """
        data = request.get_json()

        if entity_name == EntityName.CASE:
            cases = CaseService.get_lookup_cases(data['filters'])

            report_data = []
            row = []

            for case in cases:
                row.append(case.apn)
                row.append(case.full_address)
                row.append(case.client.full_name if case.client else None)
                row.append(case.assessment.assessment_value if case.assessment else None)

                report_data.append(row)
                row = []

            df = pd.DataFrame(report_data, columns=self.REPORT_COLUMNS)

            response = make_response(df.to_csv(header=self.REPORT_COLUMNS, index=False,
                                               quoting=csv.QUOTE_ALL, line_terminator='\r\n'))
            response.headers["Content-Disposition"] = "attachment; filename=lookup_report.csv"
            response.headers["Content-Type"] = "text/csv"
            return response
        else:
            pass


class CasePetitionsReportApi(DomainResource):

    def _get_file_url(self, file_id):
        if file_id:
            host_name = request.headers['Host']
            url = url_for("api.file", file_id=file_id)
            return f'{host_name}/{url}'
        return ""

    def _get_cma_page_url(self, property_id):
        if property_id:
            host_name = request.headers['Host']
            return f'{host_name}/vue/cma/{property_id}'
        return ""

    def _get_summary_rows(self, cases):
        """
        Return a list of rows with data, columns order per row is important:
            - FOLIO
            - Tentative Value
            - All 1-4
            - Good 1-4
            - Redux Proposal

        Sample:
            [
                ['474131AA0410', '2020-11111', 297890, 274478, 277854, 274478],
                ['494122271030', '2020-17717', 142180, 148822, 125562, 133990],
            ]
        """

        rows = []
        row = []
        for case in cases:
            assessment = PropertyService.get_property_last_assessment(case.property_id, tax_year=case.tax_year)
            case.assessment = assessment
            averages = CaseService.get_case_averages(case)
            workup = SingleCMAWorkups.get_primary_workup(case.id)

            good_bad_report_file_id = None
            cma_report_file_id = None
            if workup:
                good_bad_report_file_id = workup.good_bad_report_file_id
                cma_report_file_id = workup.report_file_id

            row.append(self._get_file_url(good_bad_report_file_id))
            row.append(self._get_file_url(cma_report_file_id))
            row.append(self._get_cma_page_url(case.property_id))

            row.append(case.apn or '')
            row.append(case.petition_number or '')
            row.append(assessment.value if assessment and assessment.value else '')
            row.append(averages.get('all_avg_4') or '')
            row.append(averages.get('good_avg_4') or '')

            proposed_value = ''
            if workup and workup.cma_payload:
                try:
                    proposed_value = int(workup.cma_payload['assessment_results']['proposed_assessment_value'])
                except Exception as e:
                    logging.error(f'Can not get proposed assessment value: {e.args}')

            row.append(proposed_value)
            rows.append(row)
            row = []

        return rows

    def _create_workbook(self, cases):
        # prepare data for the workbook
        rows = self._get_summary_rows(cases)
        file_path = DATA_IMPORT / 'petitions_report.xlsx'

        service = PetitionsReportService()
        service.insert_summary_worksheet_rows(rows)
        service.setup_summary_worksheet()
        service.workbook.save(file_path.as_posix())
        service.workbook.close()

        return file_path

    def post(self, entity_name):
        data = request.get_json()

        if entity_name == EntityName.CASE:

            cases = CaseService.get_lookup_cases(data['filters'])
            excel_file = self._create_workbook(cases)

            return send_file(excel_file.as_posix(), attachment_filename='petitions_report.xlsx', as_attachment=True)
        else:
            pass


class CaseReportApi(DomainResource):
    CASE_REPORT_COLUMNS = ['Folio', 'Address', 'Client name', 'Assessment value', 'Owner Full Name',
                           'Phone Number', 'Email', 'County', 'IP address', 'All Avg 1-4', 'Good Avg 1-4']

    def post(self, entity_name):
        data = request.get_json()

        if entity_name == EntityName.CASE:

            report_data = []
            row = []

            cases = CaseService.get_lookup_cases(data['filters'])
            for case in cases:
                averages = CaseService.get_case_averages(case)

                row.append(case.application.apn if case.application else None)
                row.append(case.full_address)
                row.append(case.client.full_name if case.client else None)
                row.append(case.assessment.assessment_value if case.assessment else None)
                row.append(', '.join(CaseService.get_case_owner_names(case)))
                row.append(case.client.phone_number_1 if case.client else None)
                row.append(case.client.email.email_address if case.client and case.client.email else None)
                row.append(case.county)
                row.append(case.application.sender_ip if case.application else None)
                row.append(averages.get('all_avg_4'))
                row.append(averages.get('good_avg_4'))

                report_data.append(row)
                row = []

            df = pd.DataFrame(report_data, columns=self.CASE_REPORT_COLUMNS)
            # output_dir = DATA_IMPORT / 'output'
            # output_dir.mkdir(parents=True, exist_ok=True)
            # df.to_csv(output_dir / 'case_report.csv', index=False)

            response = make_response(df.to_csv(index=False))
            response.headers["Content-Disposition"] = "attachment; filename=export.csv"
            response.headers["Content-Type"] = "text/csv"
            return response
        else:
            pass


class CaseExtendedListApi(DomainResource):
    CASE_REPORT_COLUMNS = ['Folio Number', 'Owner Name', 'Property Address', 'Legal Description']

    def post(self, entity_name):
        data = request.get_json()

        if entity_name == EntityName.CASE:

            report_data = []
            row = []

            cases = CaseService.get_lookup_cases(data['filters'])
            cases = sorted(cases, key=lambda x: x.property.apn)
            for case in cases:
                apn = case.application.apn if case.application else None
                if case.county == County.MIAMIDADE and apn:
                    apn = '-'.join([apn[:2], apn[2:6], apn[6:9], apn[9:]])
                row.append(apn)
                row.append(", ".join(CaseService.get_case_owner_names(case)).strip(", "))
                row.append(' '.join([case.address_line1 or '',
                                     case.address_line2 or '']))
                row.append(case.property.legal)  # legal description
                report_data.append(row)
                row = []

            df = pd.DataFrame(report_data, columns=self.CASE_REPORT_COLUMNS)

            response = make_response(df.to_csv(header=None,
                                               index=False,
                                               quoting=csv.QUOTE_ALL,
                                               line_terminator='\r\n'))
            response.headers["Content-Disposition"] = "attachment; filename=extended_cases_list.txt"
            response.headers["Content-Type"] = "text/csv"
            return response
        else:
            pass


class CaseListApi(DomainResource):
    CASE_REPORT_COLUMNS = ['Folio Number']

    def post(self, entity_name):
        data = request.get_json()

        if entity_name == EntityName.CASE:

            report_data = []
            row = []

            cases = CaseService.get_lookup_cases(data['filters'])
            cases = sorted(cases, key=lambda x: x.property.apn)
            for case in cases:
                apn = case.application.apn if case.application else None
                if case.county == County.MIAMIDADE and apn:
                    apn = '-'.join([apn[:2], apn[2:6], apn[6:9], apn[9:]])
                row.append(apn)
                report_data.append(row)
                row = []

            df = pd.DataFrame(report_data, columns=self.CASE_REPORT_COLUMNS)

            response = make_response(df.to_csv(header=None,
                                               index=False,
                                               quoting=csv.QUOTE_NONE,
                                               line_terminator='\r\n'))
            response.headers["Content-Disposition"] = "attachment; filename=cases_list.txt"
            response.headers["Content-Type"] = "text/csv"
            return response
        else:
            pass


class ClientTypesApi(DomainResource):
    def get(self):
        """
        Get all client types
        """
        client_types = ClientType.query.all()
        return jsonify(ClientTypeSchema().dump(client_types, many=True))


class ApplicationSourcesApi(DomainResource):
    def get(self):
        """
        Get all application source types
        """
        application_sources = ApplicationSource.query.all()
        return jsonify(ApplicationSourceSchema().dump(application_sources, many=True))


class PaymentStatusesApi(DomainResource):
    def get(self):
        """
        Get all payment statuses
        """
        payment_statuses = PaymentStatus.query.all()
        return jsonify(PaymentStatusSchema().dump(payment_statuses, many=True))


class ApplicationStatusesApi(DomainResource):
    def get(self):
        """
        Get all possible application statuses
        """
        application_statuses = ApplicationStatus.query.all()
        return jsonify(ApplicationStatusSchema().dump(application_statuses, many=True))


class PaymentTypesApi(DomainResource):
    def get(self):
        """
        Get all payment types
        """
        payments = PaymentType.query.all()
        return jsonify(PaymentTypeSchema().dump(payments, many=True))


class TagsApi(DomainResource):
    def get(self):
        """
        Get all list of tags
        """
        tags = Tag.query.all()
        return jsonify(TagSchema().dump(tags, many=True))

    @permission_required(Permission.EDIT)
    def post(self):
        """
        Create new tag
        """
        try:
            json_data = request.get_json()

            new_tag = TagSchema().load(json_data)
            new_tag.save()
        except Exception as e:
            db.session.rollback()
            response = jsonify(error=e.args)
            response.status_code = 500
            return response

        return jsonify(TagSchema().dump(new_tag))


class TagApi(DomainResource):
    def get(self, tag_id):
        """
        Get specific tag
        """
        try:
            tag = Tag.get_or_404(tag_id)
            return Response(
                response=json.dumps(TagSchema().dump(tag)),
                mimetype="application/json",
                status=200
            )
        except HTTPException:
            return Response(
                response=json.dumps({"Error": "Tag with id={} was not found".format(tag_id)}),
                mimetype="application/json",
                status=404
            )

    @permission_required(Permission.EDIT)
    def put(self, tag_id):
        """
        Update specific tag
        """
        try:
            json_data = request.get_json()
            json_data['id'] = tag_id

            updated_tag = TagSchema().load(json_data)
            updated_tag.save()
            return Response(
                response=json.dumps(TagSchema().dump(updated_tag)),
                mimetype="application/json",
                status=200
            )
        except Exception as e:
            db.session.rollback()
            return Response(
                response=json.dumps({"Error": e.args}),
                mimetype="application/json",
                status=500
            )

    @permission_required(Permission.EDIT)
    def delete(self, tag_id):
        """
        Delete specific tag
        """
        try:
            tag = Tag.get_or_404(tag_id)
            tag.delete()
            return Response(
                response=json.dumps({'status': True}),
                mimetype="application/json",
                status=200
            )
        except HTTPException:
            return Response(
                response=json.dumps({"Error": "Tag with id={} was not found".format(tag_id)}),
                mimetype="application/json",
                status=404
            )


class PhysicalApplicationsApi(DomainResource):
    @permission_required(Permission.EDIT)
    def post(self):
        apn = request.args.get('apn', type=str)
        tax_year = request.args.get('tax_year', type=int)
        county = request.args.get('county', type=str)
        client_id = request.args.get('client_id', type=int)

        marketing_code = MarketingCode.get_by(name=request.args.get('marketing_code', type=int))
        application_type = ApplicationType.get_by(name=request.args.get('application_type', type=int))

        application_type_id = application_type.id if application_type else None
        marketing_code_id = marketing_code.id if marketing_code else None

        new_app = Application(apn=apn, tax_year=tax_year, application_type_id=application_type_id, county=county,
                              marketing_code_id=marketing_code_id, client_id=client_id
                              )
        new_app.save()
        return jsonify(ApplicationSchema().dump(new_app))


class ApplicationsApi(DomainResource):
    _exclude_audit_fields = ('id', 'created_at', 'updated_at', 'created_by_id', 'updated_by_id')

    def get(self):
        """
        Get a list of all applications ordered by 'changed_status_at' date

        GET params:
        :status_id: ID of application status ('incoming', 'rejected', ...)
        :property_id: The property ID
        :tax_year: The tax year
        """
        # application status
        status_id = request.args.get('status_id', None, type=int)
        property_id = request.args.get('property_id', None, type=int)
        tax_year = request.args.get('tax_year', None, type=int)

        # get all applications
        if status_id:
            query = Application.query.filter_by(status_id=status_id)
        else:
            query = Application.query

        # filter by 'property_id'
        if property_id:
            query = query.filter(Application.property_id == property_id)

        # filter by 'tax_year'
        if tax_year:
            query = query.filter(Application.tax_year == tax_year)

        # fetch all applications ordered by creation date
        applications = query.order_by(Application.changed_status_at.desc()).all()

        # include assessment to application
        for app in applications:
            assessment = PropertyService.get_property_last_assessment(app.property_id)
            app.assessment = assessment

        return jsonify(ApplicationSchema(exclude=('original_application', 'client')).dump(applications, many=True))

    def make_blank_application(self, data):
        """
        Make blank application object
        """
        # create 'prospect' client for the application
        # new_client = Client(
        #     type_id=ClientType.PROSPECT
        # )
        # new_client.save()
        # data['client_id'] = new_client.id

        billing = CaseService.make_billing(**{})
        data['billing_id'] = billing.id

        email = CaseService.get_or_make_email(**{})
        data['email_id'] = email.id

        property_id = data.get('property_id')
        prop = db.session.query(Property).get(property_id)
        pin_code = PropertyService.generate_code(property_id) if property_id else None
        data['pin_code'] = pin_code

        # Map data for the client, application deserialization
        # Read data from 'property' model and store them into client & application via marshmallow mapping
        data['county'] = prop.county
        data['apn'] = prop.apn
        data['address_line1'] = capitalize_address(prop.address_line_1)
        data['address_line2'] = capitalize_address(prop.address_line_2)
        data['address_city'] = capitalize_address(prop.city)
        data['address_state'] = str(prop.state).upper()
        data['address_zip'] = prop.zip

        # set defaults
        data['source_id'] = ApplicationSource.MANUAL
        data['status_id'] = ApplicationStatus.INCOMING
        data['application_type_id'] = ApplicationType.STANDARD
        data['payment_type_id'] = PaymentType.CARD
        data['marketing_code_id'] = MarketingCode.NONE_CODE
        data['tax_year'] = datetime.now().year

        new_app = ApplicationSchema(exclude=self._exclude_audit_fields).load(data)
        new_app.save()

        if new_app.is_manual():
            new_app.prefill_mailing_address()
            new_app.save()

        return new_app

    @permission_required(Permission.EDIT)
    def post(self):
        """
        Create case application
        Application source can be 'digital' or 'physical'
        For each application source there is a separate handling case
        """
        try:
            # get body
            json_data = request.get_json()

            # include sender ip address into case_application
            json_data['sender_ip'] = request.remote_addr

            if Application.exists(property_id=json_data['property_id']):
                return bad_request(
                    error_type='duplicate',
                    message=Application.DUPLICATION_MESSAGE
                )

            # create blank application
            application = self.make_blank_application(json_data)

            # prepare digital application pdf for notes attachments
            pdf_file = prepare_pdf_attachment(application, signature_coords='1x42x62x150x27')
            attachment = encode_latin1_to_utf8(pdf_file)

            # create and save new system 'SUBMIT' application note
            Note.create_system_note(NoteSender.APPLICATION,
                                    application,
                                    NoteDescription.APPLICATION_SUBMITTED_MANUALLY,
                                    NoteType.SUBMITTED,
                                    attachment=attachment,
                                    attachment_extension='.pdf')

            return jsonify(ApplicationSchema().dump(application))
        except Exception as e:
            db.session.rollback()
            return server_error(e.args)


class ApplicationApi(DomainResource):

    def get(self, application_id):
        """
        Get specific application
        :param application_id: The application id
        """
        try:
            application = Application.get_or_404(application_id)
            assessment = PropertyService.get_property_last_assessment(application.property_id)
            application.assessment = assessment

            # exclude 'original_application' data to speed up loading
            return jsonify(ApplicationSchema(exclude=('original_application',)).dump(application))
        except HTTPException:
            response = jsonify(error="Application with id={} was not found".format(application_id))
            response.status_code = 404
            return response

    @permission_required(Permission.EDIT)
    def put(self, application_id):
        """
        Update specific application
        """
        try:
            # current state of the application
            current_app = Application.get(application_id)
            current_json = ApplicationSchema(exclude=('original_application',)).dump(current_app)

            # new state of the application
            json_data = request.get_json()
            json_data['id'] = application_id

            # form a note text to be saved
            note_text, fields_changed = Application.get_state_changes_text(
                current=current_json,
                target=json_data
            )

            # change email object or create new if does not exists
            if StateChangedMixin.email_changed(fields_changed):
                email_object = json_data.pop('email')
                email_address = str(email_object['email_address']).lower()
                email = CaseService.get_or_make_email(email_address=email_address)
                email.originated_from_id = EmailOriginator.MANUAL_EDIT_APPLICATION
                email.save()

                client = Client.get_by(email_id=email.id)
                if not client:
                    client = Client(
                        type_id=ClientType.PROSPECT,
                        email_id=email.id
                    )
                    client.save()

                json_data['client_id'] = client.id
                json_data['email_id'] = email.id

            # update application in database
            updated_app = ApplicationSchema().load(json_data)
            updated_app.updated_at = datetime.now()
            updated_app.updated_by_id = Application.current_user_id_or_none()
            updated_app.save()

            # create and save new system 'UPDATED' application note
            if note_text:
                Note.create_system_note(NoteSender.APPLICATION, updated_app, note_text, NoteType.UPDATED)

            return jsonify(ApplicationSchema(exclude=('original_application',)).dump(updated_app))
        except Exception as e:
            db.session.rollback()
            response = jsonify(error=e.args)
            response.status_code = 500
            return response


class ApplicationSignEmailApi(DomainResource):
    def get(self, application_id):
        application = Application.get(application_id)
        if not application:
            return not_found("Application with id={} was not found".format(application_id))

        if not application.email or not application.email.email_address:
            return bad_request(f"Application with id={application_id} does not have email address")

        try:
            if not application.signature_base64_encoded and application.is_manual():
                repair_token = application.encode_repair_token(application_id=application_id)
                application.repair_token = repair_token
                application.save()

                repair_link = CaseService.REDUX_REPAIR_URL + f'?token={application.repair_token}'
                context = {
                    'full_name': application.full_name or 'client',
                    'repair_link': repair_link
                }
                sign_email_pdf = make_and_send_email(application,
                                                     email_type=EmailToClient.sign_email,
                                                     context=context)
                # update timestamp of application sign email sent
                application.sign_email_sent_at = datetime.now()

                # add sign email pdf to application log activity
                Note.create_system_note(NoteSender.APPLICATION,
                                        application,
                                        NoteDescription.APPLICATION_SIGN_EMAIL_SENT,
                                        NoteType.EMAIL_SENT,
                                        attachment=sign_email_pdf,
                                        attachment_extension='.pdf')

            return jsonify(status='OK')
        except Exception as e:
            logger.error(e.args)


class ClientsApi(DomainResource):
    def get(self):
        """
        Get all clients
        """
        clients = Client.query.all()
        return jsonify(ClientSchema().dump(clients, many=True))

    @permission_required(Permission.EDIT)
    def post(self):
        """
        Create client
        """
        try:
            json_data = request.get_json()
            json_data['type_id'] = json_data.get('type_id', None) or ClientType.PROSPECT
            new_client = ClientSchema().load(json_data)
            new_client.save()

            return jsonify(ClientSchema().dump(new_client))
        except Exception as e:
            db.session.rollback()
            response = jsonify(error=e.args)
            response.status_code = 500
            return response


class ClientApi(DomainResource):
    def get(self, client_id):
        """
        Get specific client
        """
        try:
            client = Client.get_or_404(client_id)
            return jsonify(ClientSchema().dump(client))
        except HTTPException:
            response = jsonify(error="Client with id={} was not found".format(client_id))
            response.status_code = 404
            return response

    @permission_required(Permission.EDIT)
    def put(self, client_id):
        """
        Update specific client
        """
        try:
            current_client = Client.get(client_id)
            current_json = ClientSchema().dump(current_client)

            json_data = request.get_json()
            json_data['id'] = client_id

            # form a note text to be saved
            note_text, fields_changed = Client.get_state_changes_text(
                current=current_json,
                target=json_data
            )

            # change email object or create new if does not exists
            if StateChangedMixin.email_changed(fields_changed):
                email_object = json_data.pop('email')
                email = CaseService.get_or_make_email(email_address=email_object['email_address'])
                email.originated_from_id = EmailOriginator.MANUAL_EDIT_APPLICATION
                email.save()

                json_data['email_id'] = email.id

            updated_client = ClientSchema().load(json_data)
            updated_client.updated_at = datetime.now()
            updated_client.save()
            logging.info(f"Client with id={client_id} was updated at {datetime.now()}")

            # create and save new system 'UPDATED' client note
            if note_text:
                Note.create_system_note(NoteSender.CLIENT, updated_client, note_text, NoteType.UPDATED)

            return jsonify(ClientSchema().dump(updated_client))
        except Exception as e:
            db.session.rollback()
            response = jsonify(error=e.args)
            response.status_code = 500
            return response

    @permission_required(Permission.EDIT)
    def delete(self, client_id):
        """
        Delete specific client
        """
        try:
            client = Client.get_or_404(client_id)
            client.delete()
            logging.info(f"Client with id={client_id} was deleted at {datetime.now()}")
            return jsonify({'status': True})
        except HTTPException:
            response = jsonify(error="Client with id={} was not found".format(client_id))
            response.status_code = 404
            return response


class CasePropertiesApi(DomainResource):
    def get(self, client_id=None):
        """
        Get all properties cases or client specific properties cases
        """
        if client_id is None:
            case_properties = CaseProperty.query.all()
        else:
            case_properties = CaseProperty.query.filter_by(client_id=client_id).all()
        return jsonify(CasePropertySchema().dump(case_properties, many=True))

    @permission_required(Permission.EDIT)
    def post(self):
        """
        Create case property
        """
        try:
            json_data = request.get_json()
            new_case = CasePropertySchema().load(json_data)
            new_case.save()

            return jsonify(CasePropertySchema().dump(new_case))
        except Exception as e:
            response = jsonify(error=e.args)
            response.status_code = 500
            return response


class CasePropertiesDr486Api(DomainResource):
    def get(self, case_id=None):
        case = CaseProperty.get_or_404(case_id)
        apn = case.apn
        if case.county == County.MIAMIDADE:
            format_apn = '-'.join([apn[:2], apn[2:6], apn[6:9], apn[9:]])
        else:
            format_apn = apn
        filename = f'{format_apn}.pdf'
        dr486_pdf_report_path = helper_dr486_pdf_template(case)
        return send_file(dr486_pdf_report_path,
                         as_attachment=True,
                         attachment_filename=filename)


class CasePropertyWorkupsApi(Resource):
    def get(self, case_property_id):
        case = CaseProperty.get_or_404(case_property_id)
        return jsonify(SingleCMAWorkupsSchema(exclude=('cma_payload', )).dump(case.workups, many=True))


class CasePropertyEvidencePackageApi(DomainResource):
    def get(self, case_property_id):
        case = CaseProperty.get_or_404(case_property_id)
        output_pdf = EvidenceService().gen_evidence_package(case)

        if not output_pdf:
            return bad_request(f"Can not create evidence package document for the case with id={case_property_id}")

        with open(output_pdf, 'rb') as binary_file:
            binary_file_data = binary_file.read()

        file_name = Path(output_pdf).name

        response = make_response(binary_file_data)
        response.headers['Content-Type'] = "application/pdf"
        response.headers['Content-Disposition'] = f'inline; filename={file_name}'

        return response


class WorkupEvidencePackageApi(DomainResource):
    def get(self, workup_id):
        workup = SingleCMAWorkups.get_or_404(workup_id)
        case_property = workup.case_property

        output_pdf = EvidenceService().gen_evidence_package(case_property)
        if not output_pdf:
            return bad_request(f"Can not create evidence package document for the case with id={case_property.id}")

        with open(output_pdf, 'rb') as binary_file:
            binary_file_data = binary_file.read()

        file_name = Path(output_pdf).name

        response = make_response(binary_file_data)
        response.headers['Content-Type'] = "application/pdf"
        response.headers['Content-Disposition'] = f'inline; filename={file_name}'

        return response


class CasePropertyApi(DomainResource):
    def get(self, case_property_id):
        """
        Get specific case property
        """
        try:
            case_property = CaseProperty.get_or_404(case_property_id)
            assessment = PropertyService.get_property_last_assessment(
                property_id=case_property.property_id,
                tax_year=case_property.tax_year
            )
            case_property.assessment = assessment

            return jsonify(CasePropertySchema().dump(case_property))
        except HTTPException:
            response = jsonify(error="Case property with id={} was not found".format(case_property_id))
            response.status_code = 404
            return response

    @permission_required(Permission.EDIT)
    def put(self, case_property_id):
        """
        Update specific case property
        """
        try:
            # current state of the application
            current_case = CaseProperty.get(case_property_id)
            current_json = CasePropertySchema().dump(current_case)

            json_data = request.get_json()
            json_data['id'] = case_property_id

            # form a note text to be saved
            note_text, fields_changed = CaseProperty.get_state_changes_text(
                current=current_json,
                target=json_data
            )

            updated_case = CasePropertySchema().load(json_data)
            updated_case.updated_at = datetime.now()
            updated_case.updated_by_id = CaseProperty.current_user_id_or_none()

            if updated_case.application:
                updated_case.application.payment_type_id = updated_case.payment_type_id
                updated_case.application.payment_status_id = updated_case.payment_status_id

            updated_case.save()
            logging.info(f"CaseProperty with id={case_property_id} was updated at {datetime.now()}")

            # create and save new system 'UPDATED' application note
            if note_text:
                Note.create_system_note(NoteSender.CASE_PROPERTY, updated_case, note_text, NoteType.UPDATED)

            return jsonify(CasePropertySchema().dump(updated_case))
        except Exception as e:
            response = jsonify(error=e.args)
            response.status_code = 500
            return response

    @permission_required(Permission.EDIT)
    def delete(self, case_property_id):
        """
        Delete specific case property
        """
        try:
            case_property = CaseProperty.get_or_404(case_property_id)
            case_property.delete()
            logging.info(f"CaseProperty with id={case_property_id} was deleted at {datetime.now()}")
            return jsonify({'status': True})
        except HTTPException:
            response = jsonify(error="Property with id={} was not found".format(case_property_id))
            response.status_code = 404
            return response


class ApplicationNotesApi(DomainResource):
    def get(self, application_id):
        """
        Get all notes for the specific application
        """
        app = Application.get(application_id)
        if not app:
            return not_found("Application with id={} was not found".format(application_id))

        # application log activity
        notes = app.notes

        # get application email object and retrieve email bounce activity if any
        email = CaseEmail.get(app.email_id)
        notes = notes + email.notes

        # sort notes by creation date
        notes = sorted(notes, key=attrgetter('created_at'), reverse=True)

        return jsonify(NoteSchema(exclude=('attachment',)).dump(notes, many=True))

    @permission_required(Permission.EDIT)
    def post(self, application_id):
        """
        Create note for the specific application
        """
        app = Application.get(application_id)
        if not app:
            return not_found("Application with id={} was not found".format(application_id))

        try:
            json_data = request.get_json()
            json_data['sender'] = NoteSender.APPLICATION
            json_data['sender_id'] = application_id
            json_data["type_id"] = NoteType.MANUAL

            # create & persist new note for the application object
            new_note = Note.create_note(**json_data)
            return jsonify(NoteSchema().dump(new_note))
        except Exception as e:
            db.session.rollback()
            response = jsonify(error=e.args)
            response.status_code = 500
            return response


class ClientNotesApi(DomainResource):
    def get(self, client_id):
        """
        Get all notes for the specific client
        """
        client = Client.get(client_id)
        if not client:
            return not_found("Client with id={} was not found".format(client_id))

        # get client log activity
        notes = client.notes

        # add application log activity that was approved for this client
        for app in client.applications:
            if app.client_id == client.id:
                notes = notes + app.notes

        # add all client cases log activity
        for cp in client.case_properties:
            notes = notes + cp.notes

        # sort notes by creation date
        notes = sorted(notes, key=attrgetter('created_at'), reverse=True)

        return jsonify(SenderNoteSchema(exclude=('attachment',)).dump(notes, many=True))

    @permission_required(Permission.EDIT)
    def post(self, client_id):
        """
        Create note for the specific client
        """
        client = Client.get(client_id)
        if not client:
            return not_found("Client with id={} was not found".format(client_id))

        try:
            json_data = request.get_json()
            json_data['sender'] = NoteSender.CLIENT
            json_data['sender_id'] = client_id
            json_data["type_id"] = NoteType.MANUAL

            # create & persist new note for the client object
            new_note = Note.create_note(**json_data)
            return jsonify(NoteSchema().dump(new_note))
        except Exception as e:
            db.session.rollback()
            response = jsonify(error=e.args)
            response.status_code = 500
            return response


class CasePropertyNotesApi(DomainResource):
    def get(self, case_property_id):
        """
        Get all notes for the specific case property
        """
        case_property = CaseProperty.get(case_property_id)
        if not case_property:
            return not_found("Case property with id={} was not found".format(case_property_id))

        # sort notes by creation date
        notes = sorted(case_property.notes, key=attrgetter('created_at'), reverse=True)
        return jsonify(SenderNoteSchema(exclude=('attachment',)).dump(notes, many=True))


class NoteApi(DomainResource):
    def get(self, note_id):
        """
        Get specific note
        :param note_id: The note id
        """
        try:
            note = Note.get_or_404(note_id)
            return jsonify(NoteSchema().dump(note))
        except HTTPException:
            response = jsonify(error="Note with id={} was not found".format(note_id))
            response.status_code = 404
            return response

    @permission_required(Permission.EDIT)
    def put(self, note_id):
        """
        Update specific note
        :param note_id: The note id
        """
        try:
            json_data = request.get_json()
            json_data['id'] = note_id

            updated_note = NoteSchema().load(json_data)
            updated_note.updated_at = datetime.now()
            updated_note.save()

            return jsonify(NoteSchema().dump(updated_note))
        except Exception as e:
            db.session.rollback()
            return server_error(e.args[0])

    @permission_required(Permission.EDIT)
    def delete(self, note_id):
        """
        Delete specific note
        :param note_id: The note id
        """
        try:
            note = Note.get_or_404(note_id)
            note.delete()
            return jsonify(status=True)
        except HTTPException:
            return not_found("Note with id {} was not found".format(note_id))


class ApplicationTypesApi(DomainResource):
    def get(self):
        """
        Get list of application types
        """
        application_types = ApplicationType.query.all()
        return jsonify(ApplicationTypeSchema().dump(application_types, many=True))


class MarketingCodeApi(DomainResource):
    def get(self):
        """
        Get list of marketing codes
        """
        marketing_codes = MarketingCode.query.all()
        return jsonify(MarketingCodeSchema().dump(marketing_codes, many=True))


class ApplicationDuplicationsApi(DomainResource):
    def get(self, application_id):
        """
        Get application duplicates
        """
        application = Application.get_by(id=application_id)
        if not application:
            return not_found("Application with id={} was not found".format(application_id))
        return jsonify(application.get_duplication_urls())


class PropertyHistoryApi(DomainResource):

    def make_property_history(self, objects, history, tax_years, application, assessment_type):
        """
        Make a property history record
        """
        property_id = application.property_id
        applicant_name = None
        client_id = None
        for obj in objects:
            o = obj[0]
            a = obj[1]
            ad = obj[2]

            if ad.tax_year not in tax_years and a.assessment_type == assessment_type:
                tax_years.append(ad.tax_year)

                clients = (
                    db.session.query(Client).join(ClientType).join(
                        CaseProperty).filter(
                        CaseProperty.property_id == property_id).filter(
                        CaseProperty.tax_year == ad.tax_year).filter(
                        ClientType.id == ClientType.CURRENT)
                ).order_by(Client.created_at.desc()).all()

                if len(clients) > 1:
                    print("Found more than one valid client for the property with id={}".format(property_id))
                if clients:
                    applicant_name = str(clients[0].full_name)
                    client_id = clients[0].id

                history_record = {
                    'property_id': property_id,
                    'application_id': application.id,
                    'assessment_type': a.assessment_type,
                    'tax_year': ad.tax_year,
                    'first_full_name': str(o.first_full_name),
                    'second_full_name': str(o.second_full_name),
                    'applicant_name': applicant_name,
                    'is_client': True if applicant_name else False,
                    'client_id': client_id
                }
                history.append(history_record)

        return history

    def get(self, application_id):
        """
        Get history for application property
        The count of property history records is how much assessments you have for this property
        for different tax year.

        'Final' assessments have the highest priority and if no 'final' assessment for the tax year,
        then 'tent' assessment will take as the property history record.

        For example:
            * if you have 'final' 2020 and 'tent' 2020 --> 'final' 2020 will use for the 2020
            * if you have 'tent' 2019 only --> 'tent' 2019 will use for the 2019

        """
        # property history
        history = []

        application = Application.get(application_id)
        if not application:
            return not_found("Application with id={} was not found".format(application_id))

        property_id = application.property_id
        if not property_id:
            # return bad_request("Invalid property_id for the application with id={}".format(application_id))
            return jsonify(history)

        query = (
            db.session.query(Owner, Assessment, AssessmentDate).join(
                Assessment, Owner.property_id == Assessment.property_id).join(
                AssessmentDate, Assessment.assessment_id == AssessmentDate.id).filter(
                Owner.property_id == property_id).filter(
                Owner.data_source == 'assessment').order_by(
                AssessmentDate.valuation_date.desc())
        )
        # fetch all joined objects
        objects = query.all()

        # unique tax years
        tax_years = []

        try:
            # use 'final' assessment as a priority
            history = self.make_property_history(objects, history, tax_years, application,
                                                 assessment_type=Assessment.FINAL)

            # use 'tent' assessment if 'final' not found for the 'tax_year'
            history = self.make_property_history(objects, history, tax_years, application,
                                                 assessment_type=Assessment.TENT)

            # sort by 'tax_year' desc
            sorted_history = sorted(history, key=itemgetter('tax_year'), reverse=True)
            return jsonify(sorted_history)
        except ServerError as e:
            response = jsonify(error=e.args)
            response.status_code = 500
            return response


class ApplicationApproveApi(DomainResource):

    @permission_required(Permission.EDIT)
    def put(self, application_id):
        """
        Approve application
            * Approve application and change application status  to 'APPROVED'
            * The 'PROSPECT' client of application change to 'CURRENT'
            * New Case Property object create for the current property
            * Create System Note, that application approved
            * Assign unique 6 characters ID for the client and case property objects
        """
        try:

            # update application status to 'APPROVED'
            app = CaseService.update_application_status(application_id, status=ApplicationStatus.APPROVED)

            # update timestamp
            app.updated_at = datetime.now()
            app.updated_by_id = Application.current_user_id_or_none()

            # update client to 'CURRENT'
            case_client = CaseService.make_case_client(app)
            app.client_id = case_client.id
            app.client = case_client
            app.save()

            # create & persist new case property object
            case_property = CaseService.make_case_property(app)

            # link current application to case property
            app.case_property_id = case_property.id
            app.case_property = case_property

            # create check payment invoice record
            # new_invoice = PaymentInvoice(case_application_id=app.id,
            #                              case_client_id=case_client.id,
            #                              type='check')
            # db.session.add(new_invoice)

            # persist changes
            app.save()

            # prepare pdfs to be attached in the email
            attachment_latin1_encoded = prepare_pdf_attachment(app, signature_coords='1x42x62x150x27')
            attachment = encode_latin1_to_utf8(attachment_latin1_encoded)

            Note.create_system_note(NoteSender.APPLICATION,
                                    app,
                                    NoteDescription.APPLICATION_APPROVED_CONTRACT,
                                    NoteType.APPROVED_CONTRACT,
                                    attachment=attachment,
                                    attachment_extension='.pdf')

            # prepare the invoice to be attached in the email
            # if app.is_check_payment():
            #     invoice_pdf_attachment = invoice_pdf(app, new_invoice)
            # elif app.is_credit_card_payment() and not app.is_paid():
            #     new_invoice.type = 'credit_card'
            #     db.session.add(new_invoice)
            #     invoice_pdf_attachment = invoice_pdf(
            #         app, new_invoice, template='ReduxInvoiceCreditCard.pdf')
            # else:
            #     invoice_pdf_attachment = None

            # if invoice_pdf_attachment:
            #     with open(invoice_pdf_attachment, 'rb') as f:
            #         invoice_pdf_binary = f.read()
            #         invoice_pdf_binary = invoice_pdf_binary.decode('latin-1').encode('utf-8')
            #     Note.create_system_note(NoteSender.APPLICATION,
            #                             app,
            #                             'Check invoice sent as an email attachment',
            #                             NoteType.APPROVED,
            #                             attachment=invoice_pdf_binary,
            #                             attachment_extension='.pdf')

            # send email to client
            email_context = CaseService.get_email_context(app)
            email_to_be_sent = EmailService.what_email_to_send(app)
            send_email(app.email.email_address, email_to_be_sent, attachment=attachment_latin1_encoded, **email_context)

            # create html email pdf binary
            html_string = render_template(email_to_be_sent.template_path + '.html', **email_context)
            pdf_binary = pdfkit.from_string(html_string, False, ).decode('ISO-8859-1').encode('utf-8')

            # create and save new system 'APPROVE' application note
            Note.create_system_note(NoteSender.APPLICATION,
                                    app,
                                    NoteDescription.APPLICATION_APPROVED,
                                    NoteType.APPROVED,
                                    attachment=pdf_binary,
                                    attachment_extension='.pdf')

            return jsonify(ApplicationSchema(exclude=('original_application',)).dump(app))
        except NotFoundError as e:
            return not_found(e.args)
        except Exception as e:
            db.session.rollback()
            response = jsonify(error=e.args)
            response.status_code = 500
            return response


class ApplicationRejectApi(DomainResource):
    @permission_required(Permission.EDIT)
    def put(self, application_id):
        """
        Reject application
        """
        try:
            # update application status to 'REJECTED'
            app = CaseService.update_application_status(application_id, status=ApplicationStatus.REJECTED)

            # update timestamp
            app.updated_at = datetime.now()
            app.updated_by_id = Application.current_user_id_or_none()

            # persist changes
            app.save()

            # create and save new system 'REJECTED' application note
            Note.create_system_note(NoteSender.APPLICATION, app,
                                    NoteDescription.APPLICATION_REJECTED.format(app.reject_reason.name),
                                    NoteType.REJECTED)
            return jsonify(ApplicationSchema(exclude=('original_application',)).dump(app))
        except NotFoundError as e:
            return not_found(e.args)
        except Exception as e:
            db.session.rollback()
            response = jsonify(error=e.args)
            response.status_code = 500
            return response


class ApplicationReviewApi(DomainResource):
    @permission_required(Permission.EDIT)
    def put(self, application_id):
        """
        Review application
        """
        try:
            # update application status to 'REVIEWED'
            app = CaseService.update_application_status(application_id, status=ApplicationStatus.REVIEWED)

            # update timestamp
            app.updated_at = datetime.now()
            app.updated_by_id = Application.current_user_id_or_none()

            # persist changes
            app.save()

            # create and save new system 'REJECTED' application note
            Note.create_system_note(
                NoteSender.APPLICATION, app,
                NoteDescription.APPLICATION_REVIEWED,
                NoteType.REVIEWED
            )
            return jsonify(ApplicationSchema(exclude=('original_application',)).dump(app))
        except NotFoundError as e:
            return not_found(e.args)
        except Exception as e:
            db.session.rollback()
            response = jsonify(error=e.args)
            response.status_code = 500
            return response


class ApplicationFullyRejectApi(Resource):
    @permission_required(Permission.EDIT)
    def put(self, application_id):
        try:
            # update application status to 'FULLY REJECTED'
            app = CaseService.update_application_status(application_id, status=ApplicationStatus.FULLY_REJECTED)

            # update timestamp
            app.updated_at = datetime.now()
            app.updated_by_id = Application.current_user_id_or_none()

            # persist changes
            app.save()

            context = dict(full_name=app.first_name)
            send_email(app.email.email_address,
                       EmailToClient.rejected,
                       **context)

            # create and save new system 'REJECT' application note
            Note.create_system_note(
                NoteSender.APPLICATION,
                app,
                NoteDescription.APPLICATION_REJECTED.format(app.reject_reason.name),
                NoteType.FULLY_REJECTED)
            return jsonify(ApplicationSchema(exclude=('original_application',)).dump(app))
        except NotFoundError as e:
            return not_found(e.args)
        except Exception as e:
            db.session.rollback()
            response = jsonify(error=e.args)
            response.status_code = 500
            return response


class ApplicationRepairApi(DomainResource):
    def get(self, application_id):
        """
        Get repair application token
        """
        try:
            # get application and generate the repair token
            application = Application.get_or_404(application_id)
            repair_token = application.encode_repair_token(application_id=application.id)

            # store token into database for further comparing
            application.repair_token = repair_token
            application.save()

            return jsonify(token=repair_token)
        except HTTPException:
            response = jsonify(error="Application with id={} was not found".format(application_id))
            response.status_code = 404
            return response


class RejectReasonsApi(DomainResource):
    def get(self):
        """
        Get list of reject reasons
        """
        reasons = RejectReason.query.all()
        return jsonify(RejectReasonSchema().dump(reasons, many=True))


class CaseInfoApi(DomainResource):

    def get_application_ids(self, status):
        ids = [
            id for id, in db.session.query(Application.id).filter(
                Application.status_id == status
            ).order_by(Application.changed_status_at.desc()).all()
        ]
        return ids

    def get(self):
        """
        Get case info

        The example of the response:
        {
            "incoming": {
                "count": 139,
                "applications": [
                    12355, 52439, 3635226, ...
                ]
            },
        }

        """
        incoming = self.get_application_ids(status=ApplicationStatus.INCOMING)
        approved = self.get_application_ids(status=ApplicationStatus.APPROVED)
        rejected = self.get_application_ids(status=ApplicationStatus.REJECTED)
        reviewed = self.get_application_ids(status=ApplicationStatus.REVIEWED)
        fully_rejected = self.get_application_ids(status=ApplicationStatus.FULLY_REJECTED)

        incoming_counts = len(incoming)
        rejected_counts = len(rejected)
        reviewed_counts = len(reviewed)
        approved_counts = len(approved)
        fully_rejected_counts = len(fully_rejected)

        return jsonify(
            {
                "incoming": {
                    "count": incoming_counts,
                    "applications": incoming
                },
                "approved": {
                    "count": approved_counts,
                    "applications": approved
                },
                "rejected": {
                    "count": rejected_counts,
                    "applications": rejected
                },
                "reviewed": {
                    "count": reviewed_counts,
                    "applications": reviewed
                },
                "fully_rejected": {
                    "count": fully_rejected_counts,
                    "applications": fully_rejected
                },
            }
        )


class ApplicationAttachmentApi(DomainResource):

    def get(self, application_id):
        """
        Get the application pdf file
        """
        app = Application.get(application_id)
        if not app:
            return not_found("Application with id={} was not found".format(application_id))

        notes = Note.get_contract_notes(app)

        if not notes:
            logger.error(f"The attachment file for the application with id={application_id} was not found")
            return jsonify(error=f"The attachment file for the application with id={application_id} was not found")
        elif len(notes) > 1:
            logger.error(f"Found multiple scan notes for the application with id={application_id}")
            return jsonify(f"Found multiple attachments for the application with id={application_id}")

        attachment = notes[0].attachment
        if not attachment:
            return jsonify(error=f"The attachment file for the application with id={application_id} was not found")

        # make sure we decode/encode in the opposite way as we encode/decode during application submitting
        response = make_response(attachment.decode('utf-8').encode('latin-1'))
        response.headers['Content-Type'] = "application/pdf"
        # response.headers['Content-Disposition'] = 'attachment; application.pdf'
        response.headers['Content-Disposition'] = 'inline; filename=application.pdf'

        return response


class SendEmailApi(DomainResource):
    def post(self):

        json_data = request.get_json()

        title = json_data.get('title', '')
        body = json_data.get('body', '')
        receiver = json_data.get('receiver')

        if not receiver:
            return jsonify(error="Receiver is not defined")

        # send email to client
        app = current_app._get_current_object()
        sender = app.config['MAIL_SENDER']
        msg = Message(title, sender=sender, recipients=[receiver])
        msg.html = body

        with app.app_context():
            mail.send(msg)

        return jsonify({'success': True})
