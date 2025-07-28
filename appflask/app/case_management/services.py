import logging
import random
import string
from datetime import datetime
from pathlib import Path

import PyPDF2
import pandas as pd
import pypdftk
import simplejson as json
from PyPDF2 import PdfFileMerger
from flask import request
from sqlalchemy import inspect

from app import db
from app.case_management.lookup import LookupCases, LookupClients
from app.case_management.models import Note, Application, ApplicationSchema, ClientType, Client, \
    CasePropertySchema, CaseProperty, ApplicationSource, ApplicationStatus, ApplicationType, MarketingCode, \
    BillingSchema, NoteSender, NoteType, PublicApplicationSchema, CompanyServing, PaymentType, ClientSchema, \
    CaseEmail, CaseEmailSchema, EmailOriginator, PhysicalApplicationSchema, CasePropertyStatus, NoteDescription
from app.database.models import Property, Files
from app.email import EmailToClient
from app.pdf.generate_pdf import QrCodeGenerator
from app.pdf.sign_pdf import prepare_pdf_attachment, encode_latin1_to_utf8
from app.routing.errors import NotFoundError
from app.routing.services import PropertyService, ScraperService, ReportService
from app.singlecma.models import SingleCMAWorkups
from app.utils.constants import County
from app.utils.fix_address import capitalize_address
from config import APP_ROOT, EVIDENCE_DIR, EVIDENCE_TEMPLATE_NAME
from my_logger import logger


class CaseService:
    REDUX_REPAIR_URL = "https://www.redux.tax/pages/repair-application-form"

    @classmethod
    def get_lookup_clients(cls, filters):
        """
        Get lookup clients
        """
        lookup_clients = LookupClients(filters)
        client_ids = lookup_clients.lookup().serialize()

        clients = [Client.get(id) for id in client_ids]
        return clients

    @classmethod
    def get_lookup_cases(cls, filters):
        """
        Get lookup cases
        """
        # lookup cases
        lookup_cases = LookupCases(filters)
        cases_ids = lookup_cases.lookup().serialize()

        # get filtered cases
        cases = [CaseProperty.get(id) for id in cases_ids]

        for case in cases:
            assessment = PropertyService.get_property_last_assessment(case.property_id, tax_year=case.tax_year)
            case.assessment = assessment

        return cases

    @classmethod
    def get_case_averages(cls, case):
        averages = {
            'all_avg_4': None,
            'good_avg_4': None
        }
        property_id = case.property_id
        if not property_id:
            return averages

        cma_result = PropertyService.get_last_mass_cma_result(property_id)
        if not cma_result:
            return averages

        if cma_result.computed_cma and cma_result.computed_cma_good_small:
            averages['all_avg_4'] = cma_result.computed_cma
            averages['good_avg_4'] = cma_result.computed_cma_good_small

        # Good Subject Sale, use formulas to calculate averages as:
        # All_Avg_1-4 = subject_sale_price - cost_of_sale
        # Good_Avg_1-4 = subject_sale_price - cost_of_sale
        #
        # savings = government assessed - (subject sale - cost of sale)
        # savings is 'subject_sale' column in 'CmaResult' table
        else:
            assessment_date_id = cma_result.task.assessment_date_id
            task_assessment = PropertyService.get_property_assessment(property_id, assessment_date_id)

            value = None
            if task_assessment and task_assessment.assessment_value and cma_result.subject_sale:
                value = task_assessment.assessment_value - cma_result.subject_sale
            averages['all_avg_4'] = value
            averages['good_avg_4'] = value

        return averages

    @classmethod
    def get_case_property_ids(cls, county=None):
        if county is None:
            cases = db.session.query(CaseProperty.id).all()
        else:
            cases = db.session.query(CaseProperty.id).filter(CaseProperty.county == county).all()

        ids = [str(c[0]) for c in cases]
        return ids

    @classmethod
    def back_fill_contact_agreement(cls):
        from manage import app
        with app.app_context():
            try:
                approved_applications = db.session.query(Application).filter(
                    Application.status_id == ApplicationStatus.APPROVED
                ).all()

                for application in approved_applications:
                    notes = application.notes

                    approved_notes = [note for note in notes if note.text == NoteDescription.APPLICATION_APPROVED]
                    if approved_notes:
                        approved_note = approved_notes[0]

                    exists = False
                    for note in notes:
                        if note.text == NoteDescription.APPLICATION_APPROVED_CONTRACT:
                            if approved_note:
                                note.created_at = approved_note.created_at
                                note.updated_at = approved_note.updated_at
                                db.session.add(note)
                                db.session.commit()
                            exists = True
                            break
                    if exists:
                        continue

                    if application.original_application:
                        attachment_latin1_encoded = prepare_pdf_attachment(
                            application, signature_coords='1x42x62x150x27')
                        attachment = encode_latin1_to_utf8(attachment_latin1_encoded)

                        print(f'application_id: {application.id}')
                        contract_note = Note.create_system_note(
                            note_sender=NoteSender.APPLICATION,
                            obj=application,
                            note_text=NoteDescription.APPLICATION_APPROVED_CONTRACT,
                            note_type=NoteType.APPROVED_CONTRACT,
                            attachment=attachment,
                            attachment_extension='.pdf'
                        )

                        # update created_at for contract note
                        for note in application.notes:
                            if note.text == NoteDescription.APPLICATION_APPROVED:
                                contract_note.created_at = note.created_at
                                contract_note.updated_at = note.updated_at
                                db.session.add(contract_note)
                                db.session.commit()
                                break

            except Exception as e:
                print(e)

    @classmethod
    def merge_email_clients(cls, email_address, drop_duplicated):
        result_proxy = db.session.execute(
            f'''
                SELECT case_client.id FROM case_client
                    LEFT JOIN case_email ce ON case_client.email_id = ce.id
                WHERE email_address='{email_address}'
                ORDER BY created_at;

            '''
        ).fetchall()
        client_ids = [client_id[0] for client_id in result_proxy]

        original_client_id = client_ids[0]
        print(original_client_id)

        for id in client_ids:

            if id == original_client_id:
                continue

            # update client case properties
            db.session.execute(
                f'''
                update case_property
                set client_id ={original_client_id}
                where client_id={id};
                '''
            )

            # update client notes
            db.session.execute(
                f'''
                update case_note
                set sender_id ={original_client_id}
                where sender=2
                and sender_id={id};

                '''
            )

            # update client applications
            db.session.execute(
                f'''
                update case_application
                set client_id = {original_client_id}
                where client_id={id};
                '''
            )

            if drop_duplicated:
                db.session.execute(
                    f'''
                    delete from case_client
                    where id={id};
                    '''
                )
            db.session.commit()

    @classmethod
    def get_or_make_email(cls, **kwargs):
        """
        Get or create email object. Ensure confirm_token always exists
        """
        try:
            email = CaseEmail.get_by(email_address=kwargs.get('email_address'))
            if not email:
                email = CaseEmailSchema().load(kwargs)
                email.save()

            if not email.confirm_token:
                email.confirm_token = cls.generate_token()

            if not email.originated_from_id:
                email.originated_from_id = EmailOriginator.APPLICATION

            email.save()
            return email
        except Exception as e:
            print(e.args)
        return None

    @classmethod
    def make_billing(cls, **kwargs):
        try:
            billing = BillingSchema().load(kwargs)
            billing.save()

            return billing
        except Exception as e:
            print(e.args)
        return None

    @classmethod
    def _translate_public_json_data(cls, json_data):
        """
        Translate public json data format for internal use
        """
        # save original request data
        json_data['original_application'] = json.dumps(PublicApplicationSchema().dump(request.get_json()))

        # get company serving
        company = CompanyServing.get_by(name=json_data.pop('company_serving'))
        json_data['company_id'] = company.id

        # get owner type
        application_type = ApplicationType.get_by(name=json_data.pop('application_type'))
        json_data['application_type_id'] = application_type.id

        application_source = ApplicationSource.get_by(name=json_data.pop('application_source', None))
        json_data['source_id'] = application_source.id if application_source else ApplicationSource.DIGITAL
        json_data['status_id'] = ApplicationStatus.INCOMING

        marketing_code = MarketingCode.get_by(name=json_data.pop('marketing_code', None))
        json_data['marketing_code_id'] = marketing_code.id if marketing_code else MarketingCode.NONE_CODE

        payment_type = PaymentType.get_by(name=json_data.pop('payment_type', None))
        json_data['payment_type_id'] = payment_type.id if payment_type else None

        property_id = json_data['property_id']
        prop = PropertyService.get_property(property_id)

        pin_code = PropertyService.generate_code(prop.id)
        json_data['pin_code'] = pin_code

        # Map data for the client, application deserialization
        # Read data from 'property' model and store them into client & application via marshmallow mapping
        json_data['county'] = prop.county
        json_data['address_line1'] = capitalize_address(prop.address_line_1)
        json_data['address_line2'] = capitalize_address(prop.address_line_2)
        json_data['address_city'] = capitalize_address(prop.city)
        json_data['address_state'] = str(prop.state).upper()
        json_data['address_zip'] = prop.zip
        json_data['apn'] = prop.apn

        json_data['mailing_line1'] = capitalize_address(json_data['mailing_line1'])
        json_data['mailing_line2'] = capitalize_address(json_data['mailing_line2'])
        json_data['mailing_line3'] = capitalize_address(json_data['mailing_line3'])
        json_data['mailing_city'] = capitalize_address(json_data['mailing_city'])

        # Adjust 0/1 values to bool type
        # Note, that if the number is not 0, bool() always returns True
        # There is validation part for 'email_alerts', 'sms_alerts_1', 'sms_alerts_2'
        json_data['sms_alerts_1'] = bool(json_data['text_updates_1'])
        json_data['sms_alerts_2'] = bool(json_data['text_updates_2'])
        json_data['authorized_signer'] = bool(json_data['authorized_signer'])
        json_data['pin_entered'] = bool(json_data['pin_entered'])
        json_data['email'] = str(json_data['email']).lower()

        email = cls.get_or_make_email(email_address=json_data.pop('email', None))
        email.alerts = bool(json_data.get('email_updates', None))
        email.originated_from_id = EmailOriginator.APPLICATION

        # when email entity created, remove email from json to avoid conflicts
        json_data['email_id'] = email.id

        # find existed client by 'email'
        client = Client.get_by(email_id=email.id)

        # if client not found by 'email' then prepare new 'prospect' client object,
        # required for application creation
        # prepare to create new 'prospect' client
        if not client:
            json_data['type_id'] = ClientType.PROSPECT
            client = ClientSchema().load(json_data)
            client.save()
        json_data['client_id'] = client.id

        # TODO: remove when public front end fix it
        if json_data.get('phone_number_2') and json_data.get('phone_number_2') == "0":
            json_data['phone_number_2'] = ""

        return json_data

    @classmethod
    def update_public_application(cls, application, json_data):
        """
        Update digital application specific fields only

        fields = (
            "email", "first_name", "last_name", "initials", "authorized_signer", "text_updates_1", "text_updates_2",
            "email_updates", "phone_number_1", "phone_number_2", "signature_base64_encoded"
        )

        """
        if json_data.get('first_name') is not None:
            application.first_name = CaseService.capitalize_name_words(json_data.get('first_name'))

        if json_data.get('last_name') is not None:
            application.last_name = CaseService.capitalize_name_words(json_data.get('last_name'))

        if json_data.get('initials') is not None:
            application.initials = str(json_data.get('initials')).upper()

        if json_data.get('phone_number_1') is not None:
            application.phone_number_1 = json_data.get('phone_number_1')

        if json_data.get('phone_number_2') is not None:
            application.phone_number_2 = json_data.get('phone_number_2')

        if json_data.get('text_updates_1') is not None:
            application.sms_alerts_1 = bool(json_data.get('text_updates_1'))

        if json_data.get('text_updates_2') is not None:
            application.sms_alerts_2 = bool(json_data.get('text_updates_2'))

        if json_data.get('authorized_signer') is not None:
            application.authorized_signer = bool(json_data.get('authorized_signer'))

        if json_data.get('signature_base64_encoded') is not None:
            # if signature changed, update timestamp
            if application.signature_base64_encoded != json_data.get('signature_base64_encoded'):
                application.signature_updated_at = datetime.now()
            application.signature_base64_encoded = json_data.get('signature_base64_encoded')

        if json_data.get('email') is not None or json_data.get('email_updates') is not None:
            email = cls.get_or_make_email(email_address=json_data.get('email') or application.email.email_address)
            email.originated_from_id = EmailOriginator.MANUAL_EDIT_APPLICATION
            email.alerts = bool(json_data.get('email_updates'))
            email.save()
            application.email_id = email.id

        application.repair_token = None
        application.status_id = ApplicationStatus.INCOMING
        application.sender_ip = request.remote_addr
        application.updated_at = datetime.now()
        application.created_by_id = Application.current_user_id_or_none()
        application.updated_by_id = Application.current_user_id_or_none()
        application.save()
        return application

    @classmethod
    def __make_application(cls, data, schema):
        # create 'application' object
        application = schema().load(data)
        application.created_by_id = Application.current_user_id_or_none()
        application.updated_by_id = Application.current_user_id_or_none()
        application.save()

        # When physical application is created
        # Pre fill mailing address
        if application.is_physical():
            application.prefill_mailing_address()
            application.prefill_property_address()

        return application

    @classmethod
    def make_digital_application(cls, json_data):
        """
        Create application object required for public API and store in database
        Application creation require case property and case client objects creation.
        """
        data = cls._translate_public_json_data(json_data)

        # create billing default data
        billing = cls.make_billing(**{})
        data['billing_id'] = billing.id
        data['signature_updated_at'] = str(datetime.now())

        return cls.__make_application(data, schema=ApplicationSchema)

    @classmethod
    def make_physical_application(cls, file_path):
        data, scan, ext, base64_encoded = QrCodeGenerator().decode_file(file_path)

        # prepare data to create application
        apn = data.get('apn')
        county = data.get('county')
        tax_year = data.get('tax_year')

        from manage import app
        with app.app_context():
            application_type = ApplicationType.get_by(name=data.get('application_type'))
            application_type_id = application_type.id if application_type else ApplicationType.get_default()
            marketing_code_id = data.get('marketing_code_id') or MarketingCode.get_default()

            prop = db.session.query(Property).filter_by(apn=apn).first()
            property_id = prop.id if prop else None
            pin_code = PropertyService.generate_code(property_id) if property_id else None

            if not property_id:
                logger.error("No 'property_id' found")
                print("Warning: no 'property_id' found")

            # create 'prospect' client for the application
            # new_client = Client(
            #     type_id=ClientType.PROSPECT
            # )
            # new_client.save()
            # client_id = new_client.id
            # logger.info(f'Created prospect client with id={client_id}')

            billing = cls.make_billing(**{})
            logger.info(f'Created billing object with id={billing.id}')

            email = cls.get_or_make_email(**{})
            logger.info(f'Get or create email with id={email.id}')

            # make original scan data
            original_data = {
                'scan_file': scan,
                'scan_extension': ext
            }

            data = {
                "original_application": json.dumps(original_data),
                "application_type_id": application_type_id,
                "tax_year": tax_year,
                "billing_id": billing.id,
                "email_id": email.id,
                "source_id": ApplicationSource.PHYSICAL,
                "status_id": ApplicationStatus.INCOMING,
                "property_id": property_id,
                # "client_id": client_id,
                "marketing_code_id": marketing_code_id,
                "apn": apn,
                "county": county,
                "scan_base64_encoded": base64_encoded,
                "sms_alerts_1": True,
                "sms_alerts_2": False,
                "pin_code": pin_code
            }

            new_app = cls.__make_application(data, schema=PhysicalApplicationSchema)
            app_id = new_app.id

            # create and save new system 'SUBMIT' application note

            Note.create_system_note(
                note_sender=NoteSender.APPLICATION,
                obj=new_app,
                note_text=NoteDescription.APPLICATION_SUBMITTED_VIA_MAIL,
                note_type=NoteType.SUBMITTED,
                attachment=scan,
                attachment_extension=ext
            )

        return app_id

    @classmethod
    def get_email_context(cls, application, token=None):
        # send email to client
        context = dict(
            full_name=application.first_name,
            token=token or cls.generate_token(),  # TODO: generate proper token
            client_id=application.case_property.case_id if application.case_property else 'N/A',
            application_id=application.id,
            address=application.property.address if application.property else '',
            payment_link=application.payment_link if application.payment_link else '#'
        )
        return context

    @classmethod
    def get_sender_notes(cls, sender_id, sender):
        """
        Get all sender notes
        """
        notes = db.session.query(Note).filter(
            Note.sender == sender,
            Note.sender_id == sender_id
        ).order_by(Note.created_at.desc()).all()

        return notes

    @classmethod
    def generate_token(cls, size=32):
        token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))
        return token

    @classmethod
    def generate_case_id(cls, size=6):
        """
        Generate a random alphanumeric ID
        """
        import string
        import secrets
        alphabet = string.ascii_letters + string.digits
        while True:
            id = ''.join(secrets.choice(alphabet) for i in range(size)).upper()

            # ensure that at least one character and one digit and id is unique in a model
            if any(c.isupper() for c in id) and any(c.isdigit() for c in id):
                break
        return id

    @classmethod
    def update_application_status(cls, application_id, status):
        app = Application.get_by(id=application_id)
        if not app:
            raise NotFoundError("Application with id={} was not found".format(application_id))

        # set application id
        json_data = request.get_json()
        json_data['id'] = application_id

        # set application status id
        json_data['status_id'] = status
        updated_app = ApplicationSchema().load(json_data)

        # update the date of application status
        updated_app.changed_status_at = datetime.now()
        updated_app.save()

        return updated_app

    @classmethod
    def capitalize_name_words(cls, name: str):
        """
        Capitalize each word of the name
        """
        splits = name.split(' ')
        for i in range(len(splits)):
            splits[i] = splits[i].lower().capitalize()

        return ' '.join(splits).strip()

    @classmethod
    def make_case_client(cls, application):
        """
        Create a valid case client object, set client type to 'CURRENT'
        Update client fields from approved application fields.
        """
        try:

            # find existed client by 'email'
            email = application.email
            client = Client.get_by(email_id=email.id)

            # if client not found by 'email' then get 'prospect' client object from application
            # else get the current client object and update fields from the last approved application
            if not client:
                client = application.client
                client.email_id = application.email_id

            # update client type from 'PROSPECT' to 'CURRENT'
            client.type_id = ClientType.CURRENT

            # if client already has 'case_id' generated stay with the same
            if not client.case_id:
                # if in any case duplicated 'case_id' found - regenerate ID
                case_id = CaseService.generate_case_id()
                while Client.get_by(case_id=case_id):
                    case_id = cls.generate_case_id()
                client.case_id = case_id

            # save approved application fields to client
            client.first_name = application.first_name
            client.last_name = application.last_name
            client.marketing_code_id = application.marketing_code_id
            client.billing_id = application.billing_id
            # client.email_id = application.email_id
            client.phone_number_1 = application.phone_number_1
            client.phone_number_2 = application.phone_number_2
            client.sms_alerts_1 = application.sms_alerts_1
            client.sms_alerts_2 = application.sms_alerts_2
            client.mailing_city = application.mailing_city
            client.mailing_state = application.mailing_state
            client.mailing_zip = application.mailing_zip
            client.mailing_line1 = application.mailing_line1
            client.mailing_line2 = application.mailing_line2
            client.mailing_line3 = application.mailing_line3
            client.created_by_id = application.updated_by_id
            client.updated_by_id = application.updated_by_id

            client.save()

            Note.create_system_note(
                note_sender=NoteSender.CLIENT,
                obj=client,
                note_text='Client Created',
                note_type=NoteType.CREATED
            )
            return client
        except Exception as e:
            print(e.args)

    @classmethod
    def make_case_property(cls, application):
        """
        Create case property
        """
        data = {
            'property_id': application.property_id,
            'client_id': application.client_id,
            'county': application.county,
            'apn': application.apn,
            'address_city': application.address_city,
            'address_state': application.address_state,
            'address_zip': application.address_zip,
            'address_line1': application.address_line1,
            'address_line2': application.address_line2,
            'tax_year': application.tax_year,
            'company_id': application.company_id,
            'pin_code': application.pin_code,
            'status_id': CasePropertyStatus.APPLICATION_APPROVED,
            'payment_type_id': application.payment_type_id,
            'payment_status_id': application.payment_status_id,
            'created_by_id': application.updated_by_id,
            'updated_by_id': application.updated_by_id

        }

        # prevent creating duplicates if case property already created before
        if application.case_property:
            data['id'] = application.case_property.id
        try:
            case_property = CasePropertySchema().load(data)

            case_id = CaseService.generate_case_id()
            while CaseProperty.get_by(case_id=case_id):
                case_id = CaseService.generate_case_id()

            case_property.case_id = case_id
            case_property.save()
            return case_property
        except Exception as e:
            print(e.args)

    @classmethod
    def get_model_changes(cls, model):
        """
        Return a dictionary containing changes made to the model since it was
        fetched from the database.

        The dictionary is of the form {'property_name': [old_value, new_value]}
        """
        state = inspect(model)
        changes = {}
        for attr in state.attrs:
            hist = state.get_history(attr.key, True)

            if not hist.has_changes():
                continue

            old_value = hist.deleted[0] if hist.deleted else None
            new_value = hist.added[0] if hist.added else None
            changes[attr.key] = [old_value, new_value]

        return changes

    @classmethod
    def get_case_owner_names(cls, case):
        owner_names = []
        if case.property and case.property.owners and case.property.owners[0]:
            owner_names = [str(case.property.owners[0].first_full_name), str(case.property.owners[0].second_full_name)]
        return owner_names


class EmailService:

    @classmethod
    def what_email_to_send(cls, application):
        if application.is_check_payment():
            return EmailToClient.thank_you_check
        if application.is_credit_card_payment() and not application.is_paid():
            return EmailToClient.thank_you_card_unpaid
        return EmailToClient.thank_you


class EvidenceService:

    @staticmethod
    def parse_hearing_row(row):
        """
        Parse hearing date row data
        """
        # parse date/time object
        date_time = row[2]

        # parse hearing date
        hearing_date = date_time.date().strftime('%m/%d/%Y')

        # parse hearing time
        hearing_time = date_time.strftime('%I:%M%p').lstrip('0')

        # parse room
        room = row[3]

        # parse petition number
        petition_number = row[4]

        # extend row with new parsed columns
        row['apn'] = row[0]
        row['hearing_date'] = hearing_date or ''
        row['hearing_time'] = hearing_time or ''
        row['board_room'] = room or ''
        row['petition_number'] = petition_number or ''

        return row[5:]

    @classmethod
    def parse_hearing_xlsx(cls, file_path, **kwargs):
        """
        Parse scheduled hearing data
        :param file_path: The excel file path
        :param kwargs: Pandas 'read_excel' function configurations
        """

        df = pd.read_excel(
            file_path,
            skiprows=13,
            usecols="C:G",
            dtype={
                "Parcel #": str,
                "Hearing Date/Time": str,
                "Room": str,
                "Petition #": str
            },
            **kwargs
        )

        try:
            df = df.apply(cls.parse_hearing_row, axis=1)
            print(df)
        except Exception as e:
            print(e.args)

        return df

    @classmethod
    def format_folio(cls, apn, county):
        """
        Format folio number
        """
        if county == County.MIAMIDADE:
            apn = '-'.join([apn[:2], apn[2:6], apn[6:9], apn[9:]])
        return apn

    def gen_cover_page(self, prop, **kwargs):
        """
        Generate cover page
        :param prop: The property object
        :param kwargs: Hearing data dict

        Return:
            - A path to generated cover page pdf file
        """
        # get county to determine the way of file generating
        county = prop.county

        # support only 'Broward' and 'Miami Dade' counties
        assert county in (County.BROWARD, County.MIAMIDADE)

        # path to cover template
        # template = Path(APP_ROOT) / 'app' / 'templates' / 'evidence' / 'ReduxCoverPage.pdf'
        # template = Path(APP_ROOT) / 'app' / 'templates' / 'evidence' / 'ReduxCoverPage_finished.pdf'
        template = Path(APP_ROOT) / 'app' / 'templates' / 'evidence' / EVIDENCE_TEMPLATE_NAME

        owner = PropertyService.get_last_owner_full_name(prop.id)

        address_city = prop.city or ''
        address_state = prop.state or ''
        address_zip = prop.zip or ''

        line1 = prop.address_line_1
        line2 = prop.address_line_2 or ''
        line3 = ' '.join([address_city, address_state, str(address_zip)])

        folio = self.format_folio(prop.apn, prop.county)

        petition_number = kwargs.get('petition_number', '')
        hearing_date = kwargs.get('hearing_date', '')
        hearing_time = kwargs.get('hearing_time', '')
        board_room = kwargs.get('board_room', '')
        current_market_value = kwargs.get('current_market_value', '')
        proposed_market_value = kwargs.get('proposed_market_value', '')
        date_submitted = datetime.now().strftime('%m/%d/%Y')

        # prepare 'Broward' specific context to fill the form
        context = {
            # first page
            'Text Field 2': owner.strip(','),
            'Text Field 3': ' '.join([line1, line2]).strip(),
            'Text Field 4': line3.strip(),
            'Text Field 5': folio,
            'Text Field 6': petition_number,
            'Text Field 7': hearing_date,
            'Text Field 8': hearing_time,
            'Text Field 9': board_room,
            'Text Field 10': current_market_value,
            'Text Field 11': proposed_market_value,
            'Text Field 12': date_submitted,

            # second page
            'Text Field 18': petition_number,
            'Text Field 17': folio,
            'Text Field 16': owner.strip(','),
            'Text Field 15': hearing_date
        }

        cover_page_pdf_path = pypdftk.fill_form(
            pdf_path=template,
            datas=context,
            out_file=EVIDENCE_DIR / f'{folio}_cover.pdf'
        )
        return cover_page_pdf_path

    def gen_application_submission(self, case):
        """
        Generate case application scan for digital, manual or physical applications
        """
        application = case.application
        binary = application.get_submission_attachment()

        if binary:
            file_path = EVIDENCE_DIR / f'application_submission_{case.property.apn}.pdf'
            with open(file_path, 'wb') as f:
                f.write(binary)
            return file_path

        return None

    def gen_workup_report(self, workup):
        """
        Generate workup report pdf
        """
        file = Files.get(workup.report_file_id)
        data = file.data

        report_file_path = None
        if data:
            report_file_path = EVIDENCE_DIR / f'cma_report_{file.name}'

            # generate report pdf file
            if report_file_path:
                with open(report_file_path, 'wb') as w:
                    w.write(data)
        return report_file_path

    def gen_evidence_package(self, case):
        """
        Generate case evidence package document
        The document consists of few documents in one:
            - 'ReduxCoverPage.pdf' from /templates/evidence
            - first page of .pdf document, scrapped from official site
            - CMA report .pdf file (CMA table + Map) from saved workup
        """
        prop = case.property
        # apn = prop.apn
        # county = prop.county

        # get latest case assessment for the case tax year
        # use that assessment to grab market value from DB as:
        #   - market_value_override, if not None
        #   - value, in other cases
        assessment = PropertyService.get_property_last_assessment(
            property_id=case.property_id,
            tax_year=case.tax_year
        )

        merger = PdfFileMerger()
        workup = SingleCMAWorkups.get_primary_workup(case_property_id=case.id)

        market_value = None
        proposed_value = None
        try:
            if workup and workup.cma_payload:
                data = workup.cma_payload
                value = int(data['assessment_results']['proposed_assessment_value'])
                proposed_value = ReportService.format_price(value)

            if assessment:
                market_value = ReportService.format_price(assessment.assessed_value)
        except Exception as e:
            print(e.args)
            import traceback
            import sys
            traceback.print_exc(file=sys.stdout)

        try:
            hearing_data = case.get_hearing_data()
            logging.info(hearing_data)
            # 1. get cover page
            cover_pdf = self.gen_cover_page(
                prop,
                current_market_value=market_value,
                proposed_market_value=proposed_value,
                **hearing_data
            )
            if cover_pdf:
                merger.append(cover_pdf.as_posix())
        except Exception as e:
            logging.error('Cover pdf not created')
            print(e.args)

        try:
            # 2. scraped pdf, all pages
            scraper_print_pdf = self.gen_scraper_print(prop)
            if scraper_print_pdf:
                # append only first page
                merger.append(scraper_print_pdf, pages=(0, 1))
        except Exception as e:
            print(e.args)

        try:
            # 3. cma report pdf (cma table + map)
            cma_report_pdf = self.gen_workup_report(workup)
            if cma_report_pdf:
                merger.append(cma_report_pdf.as_posix())
        except Exception as e:
            print(e.args)

        # 4. application submission pdf
        # try:
        #     app_submission_pdf = self.gen_application_submission(case)
        #     if app_submission_pdf:
        #         merger.append(app_submission_pdf.as_posix())
        # except Exception as e:
        #     print(e.args)
        #
        # try:
        #     # 5. dr486 pdf
        #     dr486_pdf = helper_dr486_pdf_template(case)
        #     if dr486_pdf:
        #         merger.append(dr486_pdf)
        # except Exception as e:
        #     print(e.args)

        # format .pdf output filename
        # output_pdf = (EVIDENCE_DIR / f'{EvidenceService.format_folio(apn, county)} Evidence Package.pdf').as_posix()
        output_pdf = (EVIDENCE_DIR / self.get_evidence_filename(case)).as_posix()
        merger.write(output_pdf)
        merger.close()

        return output_pdf

    def get_evidence_filename(self, case):
        """
        Get evidence package filename
        """
        base_name = 'Evidence Package.pdf'
        try:
            apn = case.property.apn
            county = case.property.county
            petition_number = case.petition_number

            if petition_number:
                return f'{petition_number} {base_name}'
            elif apn:
                return f'{EvidenceService.format_folio(apn, county)} {base_name}'
        except ValueError:
            return base_name

    def gen_scraper_print(self, prop):
        """
        Generate scraper print pdf file county specific
        """
        county = prop.county
        apn = prop.apn

        if county == County.BROWARD:
            return ScraperService().broward_evidence(apn, gen_pdf=True, gen_html=False)
        elif county == County.MIAMIDADE:
            return ScraperService().miamidade_evidence(apn, gen_pdf=True, gen_html=False)

        return None

    def remove_blank_pages(self, input_path):
        """
        Remove blank pages from pdf if any
        """
        pdf_handler = open(input_path, 'rb')

        reader = PyPDF2.PdfFileReader(pdf_handler)
        writer = PyPDF2.PdfFileWriter()

        for i in range(0, reader.getNumPages()):
            page = reader.getPage(i)

            if page.getContents():
                writer.addPage(page)

        with open(input_path, 'wb') as file:
            writer.write(file)

        return input_path
