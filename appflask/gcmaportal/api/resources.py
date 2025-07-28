import difflib
from datetime import datetime
import simplejson as json

import marshmallow
from flask import request, jsonify
from flask_restful import Resource
from flask_weasyprint import render_pdf
from werkzeug.exceptions import HTTPException

from app import db
from app.case_management.models import PublicApplicationSchema, Note, NoteSender, NoteType, Application, \
    ApplicationRepairSchema, ApplicationSchema, NoteDescription
from app.case_management.services import CaseService
from app.database.models import Property
from app.database.models.property import PublicPropertySchema
from app.email import make_and_send_email, EmailToClient
from app.pdf.generate_pdf import PdfGenerator
from app.pdf.resources import GeneratePdfApi
from app.pdf.sign_pdf import prepare_pdf_attachment, encode_latin1_to_utf8
from app.routing.errors import bad_request, not_found, multiple_found, server_error, ValidationError, ServerError
from app.routing.services import PropertyService
from app.utils.comp_utils import get_whitelisted
from app.utils.constants import County


class StatusApi(Resource):
    def get(self):
        return jsonify({
            'status': 'ok'
        })


class DigitalApplicationsApi(Resource):

    def post(self):
        """
        Create digital application
        """
        # get json data
        json_data = request.get_json()
        json_data['sender_ip'] = request.remote_addr

        # encode signature, do this before schema validation
        if json_data.get('signature_base64_encoded'):
            json_data['signature_base64_encoded'] = json_data['signature_base64_encoded'].encode('utf-8')

        # validate data
        errors = PublicApplicationSchema().validate(json_data)

        # respond validation errors
        if errors:
            return bad_request(errors)

        if Application.exists(property_id=json_data['property_id'], tax_year=json_data['tax_year']):
            return bad_request(
                error_type='duplicate',
                message=Application.DUPLICATION_MESSAGE
            )
        try:
            # create application object & respond
            application = CaseService.make_digital_application(json_data)

            # replace payment url 'APPLICATION_ID' with id of created object
            if application.payment_link:
                application.payment_link = application.payment_link.replace("APPLICATION_ID", str(application.id))
                application.save()

            # send application submission welcome email
            # send email to client
            email_context = CaseService.get_email_context(
                application=application,
                token=application.email.confirm_token if application.email else None
            )
            welcome_email_pdf = make_and_send_email(application, email_type=EmailToClient.welcome,
                                                    context=email_context)

            # create and save new system 'SUBMIT' application note
            Note.create_system_note(NoteSender.APPLICATION,
                                    application,
                                    NoteDescription.APPLICATION_RECEIVED_EMAIL_SENT,
                                    NoteType.EMAIL_SENT,
                                    attachment=welcome_email_pdf,
                                    attachment_extension='.pdf')

            # prepare digital application pdf for notes attachments
            pdf_file = prepare_pdf_attachment(application, signature_coords='1x42x62x150x27')
            digital_app_pdf_binary = encode_latin1_to_utf8(pdf_file)

            # create and save new system 'SUBMIT' application note
            Note.create_system_note(NoteSender.APPLICATION,
                                    application,
                                    NoteDescription.APPLICATION_SUBMITTED_VIA_WEB,
                                    NoteType.SUBMITTED,
                                    attachment=digital_app_pdf_binary,
                                    attachment_extension='.pdf')
            return jsonify(
                {
                    "status": 1,
                    "payload": {
                        "application_id": application.id
                    }
                }
            )
        except ServerError as e:
            return server_error(e.args[0])
        except ValidationError as e:
            return bad_request(e.args)
        except Exception as e:
            db.session.rollback()
            return server_error(e.args[0])


class DigitalApplicationApi(Resource):
    def get(self, token):
        """
        Get digital application by token
        """
        try:
            # validate repair token
            application_id = Application.decode_repair_token(token)

            # invalid token or expired
            if not isinstance(application_id, int):
                return bad_request(message=application_id)

            # get application
            application = Application.get(application_id)
            if not application or not application.repair_token or application.repair_token != token:
                return bad_request(message="Invalid token, application was not found")

            return jsonify(ApplicationRepairSchema().dump(application))
        except HTTPException:
            response = jsonify(error="Application was not found, token invalid or expired")
            response.status_code = 404
            return response

    def put(self, token):
        """
        Update application by token
        """
        # validate repair token
        application_id = Application.decode_repair_token(token)

        # invalid token or expired
        if not isinstance(application_id, int):
            return bad_request(message=application_id)

        # get application
        current_app = Application.get(application_id)

        if not current_app or not current_app.repair_token or current_app.repair_token != token:
            return bad_request(message="Application was not found, token invalid or expired")

        # current state of the application
        current_json = ApplicationSchema().dump(current_app)

        json_data = request.get_json()
        json_data['id'] = current_app.id

        # validate data
        try:
            # encode signature, do this before schema validation
            if not json_data.get('signature_base64_encoded'):
                raise marshmallow.exceptions.ValidationError(
                    field_name='signature_base64_encoded',
                    message="Missing required field 'signature_base64_encoded'"
                )
            json_data['signature_base64_encoded'] = json_data['signature_base64_encoded'].encode('utf-8')
            PublicApplicationSchema().validate_signature_base64_encoded(json_data.get('signature_base64_encoded'))
        except marshmallow.exceptions.ValidationError as e:
            return bad_request(error_type=e.field_name, message=e.messages)

        try:
            # update application object with new data
            updated_app = CaseService.update_public_application(current_app, json_data)

            # save 'original_application' data for 'manual' application
            # update 'original_application' only if its first time repairing
            if updated_app.is_manual() and not updated_app.original_application:
                updated_app.original_application = json.dumps(PublicApplicationSchema().dump(request.get_json()))
                updated_app.save()

            # create and save new system 'REPAIR' application note
            Note.create_system_note(
                note_sender=NoteSender.APPLICATION,
                obj=updated_app,
                note_text="Application Repaired",
                note_type=NoteType.REPAIRED
            )
            updated_json = ApplicationSchema().dump(updated_app)

            # form a note text to be saved
            note_text, _ = Application.get_state_changes_text(
                current=current_json,
                target=updated_json
            )

            # create and save new system 'UPDATED' application note
            if note_text:
                Note.create_system_note(NoteSender.APPLICATION, updated_app, note_text, NoteType.UPDATED)

            return jsonify(
                {
                    "status": 1,
                    "payload": {
                        "application_id": updated_app.id
                    }
                }
            )
        except Exception as e:
            db.session.rollback()
            return server_error(e.args[0])


class PublicPropertyApi(Resource):
    _include_fields = (
        'property_id', 'full_address', 'address_line1', 'address_line2', 'address_zip', 'address_street',
        'address_number', 'address_state', 'address_latitude', 'address_longitude', 'address_iscondo', 'owners',
        'address_city'
    )

    def get(self):
        """
        Get home owner information

        GET params:
            - address
            - county
            - state
            - zip
            OR
            - property_id
        """

        # 'property_id' request parameter
        property_id = request.args.get('property_id', None, type=int)

        # ignore_duplicates
        ignore_duplicates = request.args.get('ignore_duplicates', None, type=bool)

        # 'address' request parameter
        address = request.args.get('address', None, type=str)

        # code
        code = request.args.get('code', None, type=str)

        try:
            if (property_id and address) or (property_id and code) or (address and code) or \
                    (not property_id and not address and not code):
                return bad_request(message="Specify one of required parameters 'property_id' or 'address' or 'code'")
            else:
                if code:
                    property_id = PropertyService.read_code(code)
                    if not property_id:
                        return bad_request(message="Invalid code")

                county = County.get_code(request.args.get('county', None, type=str))
                state = request.args.get('state', None, type=str)
                zip_code = request.args.get('zip', None, type=int)

                args = {
                    'id': property_id,
                    'address': address,
                    'county': county,
                    'state': state,
                    'zip': zip_code
                }

                properties = PropertyService.search_properties(args)

                properties = get_whitelisted(properties)

                # no matches
                if len(properties) == 0:
                    return not_found("No property found")

                # multiply matches
                if len(properties) > 1:
                    return multiple_found("Multiple properties found")

                prop = properties[0]

                # return duplicate error if application with the 'tax_year' & 'property_id' exists
                if (not ignore_duplicates) and Application.exists(property_id=prop.id, tax_year=datetime.now().year):
                    return bad_request(
                        error_type='duplicate',
                        message=Application.DUPLICATION_MESSAGE
                    )

                prop.owner_full_names = PropertyService.get_owners_full_names(prop.id)

                return jsonify(
                    {
                        'status': 1,
                        'payload': PublicPropertySchema(only=self._include_fields).dump(prop)
                    }
                )
        except Exception as e:
            return server_error(message=e.args)


class PublicPropertiesApi(Resource):
    DEFAULT_LIMIT = 15
    _include_fields = (
        'property_id', 'full_address', 'address_line1', 'address_line2', 'address_zip', 'address_street',
        'address_number', 'address_state', 'address_latitude', 'address_longitude', 'address_iscondo',
        'address_city'
    )

    def get(self):
        """
        Get properties address suggestions
        """

        # 'address' request parameter
        address = request.args.get('address', None, type=str)

        try:
            if not address:
                return bad_request("Required parameter 'address' was not specified", error_type='missing_address')
            else:
                county = request.args.get('county', None, type=str)
                state = request.args.get('state', None, type=str)
                zip_code = request.args.get('zip', None, type=int)
                limit = request.args.get('limit', None, type=int) or self.DEFAULT_LIMIT

                # include only Florida properties
                query = db.session.query(Property).filter(Property.county.in_([County.BROWARD, County.MIAMIDADE]))

                # search by county
                if county:
                    county_code = County.get_code(county)
                    query = query.filter_by(county=county_code)

                if state:
                    query = query.filter_by(state=state)

                if zip_code:
                    query = query.filter_by(zip=zip_code)

                # search by address
                if address:
                    query = PropertyService.search_by_address(query, address, address_attribute=Property.address)

                # limit result set
                if limit:
                    query = query.limit(limit)

                # fetch objects and sort by 'id'
                properties = query.all()

                properties = get_whitelisted(properties)

                # sort result addresses by best matching
                properties = sorted(properties, key=lambda x: difflib.SequenceMatcher(
                    None, x.address, address).ratio(),
                                    reverse=True)

                # no matches
                if len(properties) == 0:
                    return not_found("No property found")

                return jsonify(
                    {
                        'status': 1,
                        'payload': {
                            'properties': PublicPropertySchema(only=self._include_fields).dump(properties, many=True)
                        }
                    }
                )
        except Exception as e:
            return server_error(message=e.args)


class PublicPdfApi(Resource):

    def get(self):
        try:
            context = GeneratePdfApi.get_context(request.args)
            pdf = PdfGenerator.from_template('pdf/pdf_template.html', context)
            response = render_pdf(pdf)

            response.headers['Content-Type'] = "application/pdf"
            # response.headers['Content-Disposition'] = 'attachment; file-output.pdf'
            response.headers['Content-Disposition'] = 'inline; filename=application.pdf'

            return response
        except Exception as e:
            print(e.args)
