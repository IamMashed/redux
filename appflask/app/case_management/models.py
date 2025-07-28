import base64
from datetime import timedelta, datetime
from io import BytesIO

import jwt
import sqlalchemy
from PIL import Image
from flask import current_app
from flask import url_for
from marshmallow import fields, ValidationError, validates, validates_schema, pre_load
from marshmallow_sqlalchemy.fields import Nested

from app import db
from app.case_management.mixins import ApplicationClientMixin, BaseMixin, AuditMixin, ApplicationCasePropertyMixin, \
    StateChangedMixin
from app.database.models import Property
from app.database.models.assessment import AssessmentModelSchema
from app.database.models.files import BytesField
from app.database.models.property import BasePropertyModelSchema
from app.settings.models import BaseSchema

# clients-tags many-to-many association
ClientTag = db.Table(
    'case_client_tag', db.Model.metadata,
    db.Column('client_id', db.Integer, db.ForeignKey('case_client.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('case_tag.id'))
)


class Tag(db.Model, BaseMixin):
    __tablename__ = 'case_tag'
    __table_args__ = (
        db.UniqueConstraint('name', name='uc_case_tag_name'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    _tag_names = [
        "PITA",
        "High Value",
        "Priority",
        "Low Profit"
    ]

    @classmethod
    def insert_tags(cls):
        for tag_name in cls._tag_names:
            cls.get_or_create(name=tag_name)
        db.session.commit()


class CompanyServing(db.Model, BaseMixin):
    """
    Client company serving model
    """
    __tablename__ = 'case_company_serving'
    id = db.Column(db.Integer, primary_key=True)

    # company name
    name = db.Column(db.String)

    # company serving applications, 1+ relationship
    applications = db.relationship('Application', backref='company', uselist=True)

    # company serving case properties, 1+ relationship
    case_properties = db.relationship('CaseProperty', backref='company', uselist=True)


class ClientType(db.Model, BaseMixin):
    __tablename__ = 'case_client_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="prospect")

    PROSPECT = 1
    CURRENT = 2

    @classmethod
    def get_default(cls):
        return cls.get(cls.PROSPECT)


class Client(db.Model, BaseMixin, ApplicationClientMixin, AuditMixin, StateChangedMixin):
    """
    Client model
    """
    __tablename__ = 'case_client'
    __table_args__ = (
        db.UniqueConstraint('case_id', name='uc_case_client_case_id'),
    )

    CURRENT = 2
    PROSPECT = 1

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.String)

    type_id = db.Column(
        db.Integer,
        db.ForeignKey("case_client_type.id", name="fk_case_client_type_id"),
    )
    type = db.relationship('ClientType')

    tags = db.relationship('Tag', secondary=ClientTag, lazy='joined')

    # client case properties, 1+ relationship
    case_properties = db.relationship('CaseProperty', cascade="all,delete", uselist=True, backref='client')

    # client applications, 1+ relationship
    applications = db.relationship('Application', cascade="all,delete", backref='client', uselist=True)
    notes = db.relationship(
        "Note",
        primaryjoin="and_(Client.id==foreign(Note.sender_id), Note.sender==2)",
        backref='client'
    )

    # default fee, %
    default_fee_percent = db.Column(db.Integer)

    hearing_date = db.Column(db.DateTime)

    def get_cases_addresses(self):
        if not self.case_properties:
            print(f'Client {self.id} missing cases')
            return []
        else:
            case_addresses = [c.full_address for c in self.case_properties if c.full_address]
            return case_addresses

    @classmethod
    def get_fields_mapper(cls, key):
        mapper = {
            "root['payment_status_id']": {
                'model': PaymentStatus,
                'attribute': 'name',
                'field': 'payment_status'
            },
            "root['payment_type_id']": {
                'model': PaymentType,
                'attribute': 'name',
                'field': 'payment_type'
            },
            "root['marketing_code_id']": {
                'model': MarketingCode,
                'attribute': 'name',
                'field': 'marketing_code'
            }
        }
        return mapper.get(key, None)


class ApplicationSource(db.Model, BaseMixin):
    __tablename__ = 'case_application_source'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    PHYSICAL = 1
    DIGITAL = 2
    MANUAL = 3


class PaymentType(db.Model, BaseMixin):
    __tablename__ = 'case_payment_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    CARD = 1
    CHECK = 2


class PaymentStatus(db.Model, BaseMixin):
    __tablename__ = 'case_payment_status'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    UNPAID = 1
    PAID = 2


class ApplicationType(db.Model, BaseMixin):
    """
    Application type model
    """
    __tablename__ = 'case_application_type'
    id = db.Column(db.Integer, primary_key=True)

    # const of 'standard' application
    STANDARD = 2

    # case application type name
    name = db.Column(db.String)

    # case owner type description
    description = db.Column(db.String)

    @classmethod
    def get_default(cls):
        return cls.STANDARD


class MarketingCode(db.Model, BaseMixin):
    __tablename__ = 'case_marketing_code'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    NONE_CODE = 1

    @classmethod
    def get_default(cls):
        return cls.NONE_CODE


class ApplicationStatus(db.Model, BaseMixin):
    __tablename__ = 'case_application_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    INCOMING = 1
    APPROVED = 2
    REJECTED = 3
    FULLY_REJECTED = 4
    REVIEWED = 5


class RejectReason(db.Model, BaseMixin):
    __tablename__ = 'case_reject_reason'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Takeover(db.Model, BaseMixin):
    __tablename__ = 'case_takeover'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer,
        db.ForeignKey('case_application.id', name="fk_case_takeover_application_id")
    )
    year = db.Column(db.Integer)
    client_id = db.Column(db.Integer)


class EmailOriginator(db.Model, BaseMixin):
    __tablename__ = 'case_email_originator'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    APPLICATION = 1
    MANUAL_EDIT_APPLICATION = 2
    MANUAL_EDIT_CLIENT = 3


class CaseEmail(db.Model, BaseMixin):
    __tablename__ = 'case_email'

    __table_args__ = (
        db.UniqueConstraint('email_address', name='uc_case_email_email_address'),
    )

    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String)
    alerts = db.Column(db.Boolean, default=False)
    originated_from_id = db.Column(
        db.Integer, db.ForeignKey('case_email_originator.id', name="fk_case_email_originator_originated_from_id")
    )
    originated_from = db.relationship('EmailOriginator', uselist=False)
    notes = db.relationship("Note", primaryjoin="and_(CaseEmail.id==foreign(Note.sender_id), Note.sender==4)")

    failed_at = db.Column(db.DateTime)
    confirmed_at = db.Column(db.DateTime)
    confirm_token = db.Column(db.String)


class Billing(db.Model, BaseMixin):
    __tablename__ = 'case_billing'

    DEFAULT_AMOUNT = 15.0

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0)
    attorney_fee = db.Column(db.Float, default=0)
    late_fee = db.Column(db.Float, default=0)
    amount = db.Column(db.Float, default=15)


class Application(db.Model, BaseMixin, ApplicationClientMixin, ApplicationCasePropertyMixin, AuditMixin,
                  StateChangedMixin):
    """
    Case application model
    """

    DUPLICATION_MESSAGE = "An application was already submitted for this property. Please give us a call at " \
                          "305-504-5094 if there was an error in your previous submission."

    # def __init__(self, **kwargs):
    #     super(Application, self).__init__(**kwargs)

    __tablename__ = 'case_application'
    id = db.Column(db.Integer, primary_key=True)

    # reference to 'ApplicationType'
    application_type_id = db.Column(
        db.Integer,
        db.ForeignKey('case_application_type.id', name="fk_case_application_type_id")
    )
    type = db.relationship('ApplicationType', uselist=False)

    # reference to 'ApplicationSource'
    source_id = db.Column(
        db.Integer,
        db.ForeignKey('case_application_source.id', name="fk_case_application_source_id")
    )
    source = db.relationship('ApplicationSource', uselist=False)

    # reference to 'CaseProperty'
    case_property_id = db.Column(
        db.Integer,
        db.ForeignKey("case_property.id", name="fk_case_application_case_property_id")
    )

    # reference to 'CaseApplicationStatus'
    status_id = db.Column(
        db.Integer,
        db.ForeignKey("case_application_status.id", name="fk_case_application_status_id")
    )
    status = db.relationship('ApplicationStatus', uselist=False)

    # reference to 'CaseClient'
    client_id = db.Column(
        db.Integer,
        db.ForeignKey("case_client.id", name="fk_case_application_client_id")
    )

    # reference to 'Users'
    assigned_to = db.Column(
        db.Integer,
        db.ForeignKey("users.id", name="fk_case_application_assigned_to")
    )

    # reference to 'RejectReason'
    reject_reason_id = db.Column(
        db.Integer,
        db.ForeignKey("case_reject_reason.id", name="fk_case_application_reject_reason_id")
    )
    reject_reason = db.relationship("RejectReason", uselist=False)
    takeovers = db.relationship("Takeover", uselist=True, order_by="desc(Takeover.year)", lazy='joined')
    notes = db.relationship(
        "Note",
        primaryjoin="and_(Application.id==foreign(Note.sender_id), Note.sender==1)",
        backref='application'
    )

    initials = db.Column(db.String)
    district = db.Column(db.String)
    section = db.Column(db.String)
    block = db.Column(db.String)
    lot = db.Column(db.String)

    scan_base64_encoded = db.Column(db.LargeBinary)
    signature_base64_encoded = db.Column(db.LargeBinary)
    signature_approved = db.Column(db.Boolean)

    sender_ip = db.Column(db.String)
    original_application = db.Column(db.JSON)
    changed_status_at = db.Column(db.DateTime, server_default=sqlalchemy.sql.func.now())
    payment_link = db.Column(db.String)
    repair_token = db.Column(db.String)
    authorized_signer = db.Column(db.Boolean, default=True)
    pin_entered = db.Column(db.Boolean, default=False)
    signature_updated_at = db.Column(db.DateTime)
    sign_email_sent_at = db.Column(db.DateTime)

    @classmethod
    def exists(cls, property_id, tax_year=None):
        """
        Check if application with specified status, property_id & tax_year already exist in the system
        :param property_id: The property id from Property model
        :param tax_year: The tax year
        """

        if tax_year is None:
            tax_year = datetime.now().year

        # query all applications for the 'property_id' & 'tax_year'
        # that are not in 'rejected' or 'fully rejected' state
        query = (
            db.session.query(Application)
            .join(ApplicationStatus, isouter=True)
            .filter(Application.property_id == property_id)
            .filter(Application.tax_year == tax_year)
            .filter(Application.status_id.notin_([ApplicationStatus.FULLY_REJECTED, ApplicationStatus.REJECTED]))
        )

        if query.count() > 0:
            return True

        return False

    def get_submission_attachment(self):
        """
        Get application submission attachment pdf file
        """
        # get log activity of application submission
        query = (
            db.session.query(Note)
            .filter(Note.sender == NoteSender.APPLICATION)
            .filter(Note.sender_id == self.id)
            .filter(Note.type_id == NoteType.SUBMITTED)
        )
        note = query.first()
        attachment = note.attachment

        if attachment:
            binary = attachment.decode('utf-8').encode('latin-1')
            return binary

        return None

    def get_payment_description(self):
        """
        Get application payment description
        """
        if self.payment_status and self.payment_type:
            payment_status_description = self.payment_status.description
            payment_type_description = self.payment_type.description

            return f'{payment_type_description} - {payment_status_description}'
        return ''

    def is_payment_info_changed(self, payment_type_id, payment_status_id):
        """
        Check whether the application payment info was changed
        """
        if self.payment_status_id == payment_status_id and self.payment_type_id == payment_type_id:
            return False
        return True

    def update_payment_info(self, payment_type_id, payment_status_id):
        if payment_type_id and payment_status_id:
            self.payment_status_id = payment_status_id
            self.payment_type_id = payment_type_id

            if self.case_property:
                self.case_property.payment_status_id = payment_status_id
                self.case_property.payment_type_id = payment_type_id

            self.save()

            # create and save new system 'PAID' application note
            payment_description = self.get_payment_description()
            Note.create_system_note(NoteSender.APPLICATION, self, f"Payment Changed to '{payment_description}'",
                                    NoteType.PAID)

    def encode_repair_token(self, application_id):
        """
        Generates the repair token
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=60, seconds=0),
                'iat': datetime.utcnow(),
                'sub': application_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('REPAIR_APPLICATION_SECRET_KEY'),
                algorithm='HS256'
            ).decode('UTF-8')
        except Exception as e:
            return e

    @staticmethod
    def decode_repair_token(token):
        """
        Decodes the repair token
        """
        try:
            payload = jwt.decode(token, current_app.config.get('REPAIR_APPLICATION_SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Repair application token expired'
        except jwt.InvalidTokenError:
            return 'Invalid application repair token'

    def is_manual(self):
        """
        Check whether the application source is 'manual'
        """
        return self.source_id == ApplicationSource.MANUAL

    def is_physical(self):
        """
        Check whether the application source is 'physical'
        """
        return self.source_id == ApplicationSource.PHYSICAL

    def is_standard(self):
        """
        Check whether the application is 'standard' type
        """
        return self.application_type_id == ApplicationType.STANDARD

    def is_check_payment(self):
        """
        Check whether the payment type is 'check'
        """
        return self.payment_type_id == PaymentType.CHECK

    def is_credit_card_payment(self):
        """
        Check whether the payment type is 'credit card'
        """
        return self.payment_type_id == PaymentType.CARD

    def is_paid(self):
        """
        Check whether the payment status is 'paid'
        """
        return self.payment_status_id == PaymentStatus.PAID

    def prefill_property_address(self):
        if self.property:
            self.address_line1 = self.property.address_line_1
            self.address_line2 = self.property.address_line_2
            self.address_zip = self.property.zip
            self.address_state = self.property.state
            self.address_city = self.property.city

    def prefill_client_fields(self, client_id):
        client = Client.get(client_id)
        if client:
            self.first_name = client.first_name
            self.last_name = client.last_name
            self.email = client.email
            self.phone_number_1 = client.phone_number_1
            self.phone_number_2 = client.phone_number_2
            self.sms_alerts_1 = client.sms_alerts_1
            self.sms_alerts_2 = client.sms_alerts_2

    def prefill_mailing_address(self, owner=None):
        """
        Prefill mailing address of the application
        """
        from app.routing.services import PropertyService

        # If "Standard" application: same as the mailing address of the house owner.
        if owner is None and self.property_id is None:
            return
        elif owner is None:
            owner = PropertyService.get_property_owners(self.property_id)[0]

        if self.is_standard() or self.is_manual():
            if owner:
                self.mailing_line1 = self.mailing_line1 or owner.owner_address_1
                self.mailing_line2 = self.mailing_line2 or owner.owner_address_2
                self.mailing_line3 = self.mailing_line3 or owner.owner_address_3
                self.mailing_city = self.mailing_city or owner.owner_city
                self.mailing_state = self.mailing_state or owner.owner_state
                self.mailing_zip = self.mailing_zip or owner.owner_zip

                if not self.mailing_line2 and not self.mailing_line3:
                    mailing_city = self.mailing_city or ''
                    mailing_state = self.mailing_state or ''
                    mailing_zip = str(self.mailing_zip) if self.mailing_zip else ''
                    self.mailing_line3 = f'{mailing_city}, {mailing_state} {mailing_zip}'
            # no owner found, pre fill mailing address from full property address
            else:
                self.mailing_line1 = self.property.address

        # If mailing address is empty or the application is not "standard"
        # then fill with the property address itself.
        elif not self.is_standard() or not self.mailing_line1:
            self.mailing_line1 = self.property.address

    def get_duplication_urls(self):
        """
        Get duplicates for 'Incoming' & 'Approved' statuses
        """
        applications = db.session.query(Application).join(ApplicationStatus).filter(
            ApplicationStatus.id.notin_(
                (ApplicationStatus.REJECTED, ApplicationStatus.FULLY_REJECTED)
            ),
            Application.property_id == self.property_id,
            Application.tax_year == self.tax_year
        ).all()

        # no duplicates found
        if len(applications) == 1:
            return {}

        duplicates = {
            ApplicationStatus.INCOMING: [],
            ApplicationStatus.APPROVED: []
        }
        for app in applications:
            if app.status.id == ApplicationStatus.INCOMING:
                app_url = url_for("api.case_application", application_id=app.id)
                duplicates[ApplicationStatus.INCOMING].append(app_url)
            elif app.status.id == ApplicationStatus.APPROVED:
                app_url = url_for("api.case_application", application_id=app.id)
                duplicates[ApplicationStatus.APPROVED].append(app_url)

        return duplicates

    @classmethod
    def get_fields_mapper(cls, key):
        mapper = {
            "root['application_type_id']": {
                'model': ApplicationType,
                'attribute': 'name',
                'field': 'application_type'
            },
            "root['payment_status_id']": {
                'model': PaymentStatus,
                'attribute': 'name',
                'field': 'payment_status'
            },
            "root['payment_type_id']": {
                'model': PaymentType,
                'attribute': 'name',
                'field': 'payment_type'
            },
            "root['marketing_code_id']": {
                'model': MarketingCode,
                'attribute': 'name',
                'field': 'marketing_code'
            },
            "root['source_id']": {
                'model': ApplicationSource,
                'attribute': 'name',
                'field': 'application_source'
            },
            "root['status_id']": {
                'model': ApplicationStatus,
                'attribute': 'name',
                'field': 'application_status'
            }

        }
        return mapper.get(key, None)


class CaseAssessmentState(db.Model, BaseMixin):
    """
    Case assessment state model
    """
    __tablename__ = 'case_assessment_state'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class CasePropertyStatus(db.Model, BaseMixin):
    __tablename__ = 'case_property_status'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    status_order = db.Column(db.Integer)

    APPLICATION_APPROVED = 1


class CaseProperty(db.Model, BaseMixin, ApplicationCasePropertyMixin, AuditMixin, StateChangedMixin):
    """
    Case property model
    """
    __tablename__ = 'case_property'
    __table_args__ = (
        db.UniqueConstraint('case_id', name='uc_case_property_case_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.String)

    # reference to 'CaseClient' model
    client_id = db.Column(
        db.Integer,
        db.ForeignKey("case_client.id", name="fk_case_property_client_id")
    )

    # reference to 'CasePropertyStatus'
    status_id = db.Column(
        db.Integer,
        db.ForeignKey("case_property_status.id", name="fk_case_property_status_id")
    )
    status = db.relationship("CasePropertyStatus", uselist=False)

    # case property applications, 1+ relationship
    application = db.relationship('Application', backref='case_property', cascade="all,delete", uselist=False)
    notes = db.relationship(
        "Note",
        primaryjoin="and_(CaseProperty.id==foreign(Note.sender_id), Note.sender==3)",
        backref='case_property'
    )

    petition_number = db.Column(db.String)
    hearing_date = db.Column(db.DateTime)
    hearing_time = db.Column(db.Time)
    board_room = db.Column(db.String)

    def get_hearing_data(self):
        """
        Get case hearing data dictionary object
        """
        hearing_date = ''
        hearing_time = ''

        # format hearing date
        if self.hearing_date:
            hearing_date = self.hearing_date.date().strftime('%m/%d/%Y')

        # format hearing time
        if self.hearing_time:
            hearing_time = self.hearing_time.strftime('%I:%M%p').lstrip('0')

        return dict(
            hearing_date=hearing_date,
            hearing_time=hearing_time,
            board_room=self.board_room or '',
            petition_number=self.petition_number or ''
        )

    @classmethod
    def get_fields_mapper(cls, key):
        mapper = {
            "root['payment_status_id']": {
                'model': PaymentStatus,
                'attribute': 'name',
                'field': 'payment_status'
            },
            "root['payment_type_id']": {
                'model': PaymentType,
                'attribute': 'name',
                'field': 'payment_type'
            },
        }
        return mapper.get(key, None)


class Note(db.Model, BaseMixin, AuditMixin):
    """
    Case note model designed to store sender activity log.
    The class handle Application, Client, CaseProperty types of objects activity
    """

    __tablename__ = 'case_note'
    id = db.Column(db.Integer, primary_key=True)

    # note 'NoteType' - the type of activity: Manual or System in general
    type_id = db.Column(
        db.Integer,
        db.ForeignKey("case_note_type.id", name="fk_case_note_type_id")
    )
    type = db.relationship('NoteType')

    # reference to 'NoteSender'
    # NoteSender is a ID of object that creates a note,
    # this is a reference to NoteSender, 1 means Application , etc
    sender = db.Column(
        db.Integer,
        db.ForeignKey('case_note_sender.id', name='fk_case_note_sender'),
    )

    # id value of sender type
    # for example if a sender is Application, then sender_id is a id of the application object
    sender_id = db.Column(db.Integer)

    # Note text, the message we store as activity
    text = db.Column(db.String)

    attachment = db.Column(db.LargeBinary)
    attachment_extension = db.Column(db.String)

    @classmethod
    def create_note(cls, **kwargs):
        """
        Create custom note
        :param kwargs: a dictionary passed into Note() constructor
        """
        kwargs.pop('id', None)
        kwargs.pop('created_at', None)
        kwargs.pop('updated_at', None)

        note = NoteSchema().load(kwargs)
        note.save()

        return note

    @classmethod
    def create_system_note(cls, note_sender: int, obj, note_text: str, note_type: int,
                           attachment=None, attachment_extension=None):
        """
        Create system note

        :param note_sender: The ID of NoteSender
        :param obj: The object that send the note
        :param note_text: Text message
        :param note_type: The ID of NoteType
        :param attachment: Attachment in bytes
        :param attachment_extension: The attached file extension (pdf, doc, json etc.)
        """
        created_by_id = None
        if obj and hasattr(obj, 'created_by') and obj.created_by:
            created_by_id = obj.created_by.id

        kwargs = {
            "created_by_id": created_by_id,
            "sender": note_sender,
            "sender_id": obj.id,
            "text": note_text,
            "type_id": note_type,
            "updated_by_id": created_by_id,
            "attachment": attachment,
            "attachment_extension": attachment_extension
        }
        note = cls.create_note(**kwargs)
        return note

    @classmethod
    def get_contract_notes(cls, app):
        # check the note of approved application first
        query = (
            db.session.query(cls).filter(
                cls.sender == NoteSender.APPLICATION).filter(
                cls.sender_id == app.id).filter(
                cls.type_id == NoteType.APPROVED_CONTRACT).filter(
                cls.text == NoteDescription.APPLICATION_APPROVED_CONTRACT)
        )
        notes = query.all()

        # if no approved applications get pdf of submitted application
        if not notes:
            query = (
                db.session.query(cls).filter(
                    cls.sender == NoteSender.APPLICATION).filter(
                    cls.sender_id == app.id).filter(
                    cls.type_id == NoteType.SUBMITTED)
            )
            notes = query.all()
        return notes


class NoteSender(db.Model, BaseMixin):
    """
    Class describe a sender object that creates a notes activity
    """
    __tablename__ = 'case_note_sender'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    APPLICATION = 1
    CLIENT = 2
    CASE_PROPERTY = 3
    CASE_EMAIL = 4
    ROBOT = 5  # used for daily emails of new applications amount

    notes = db.relationship("Note", uselist=True)


class PaymentInvoice(db.Model):
    __tablename__ = 'case_payment_invoice'

    id = db.Column(db.Integer, primary_key=True)
    case_application_id = db.Column(db.ForeignKey('case_application.id', ondelete='cascade'))
    case_client_id = db.Column(db.ForeignKey('case_client.id', ondelete='cascade'))
    created_on = db.Column(db.DateTime, default=datetime.now())
    type = db.Column(db.String)  # check or credit_card

    application = db.relationship('Application', backref='check_payment_invoice')
    client = db.relationship('Client', backref='check_payment_invoice')


class NoteDescription(object):
    APPLICATION_SUBMITTED = "Application Submitted"
    APPLICATION_APPROVED = "Application Approved"
    APPLICATION_APPROVED_CONTRACT = "Contract Agreement Attachment was sent"
    APPLICATION_REVIEWED = "Application moved to Approved For Review"
    APPLICATION_REJECTED = "Application Rejected({})"
    APPLICATION_RECEIVED_EMAIL_SENT = "Application Received Email Sent"
    APPLICATION_SIGN_EMAIL_SENT = "Application Sign Email Sent"
    APPLICATION_SUBMITTED_VIA_WEB = "Application Submitted via Web"
    APPLICATION_SUBMITTED_MANUALLY = "Application Submitted Manually"
    APPLICATION_SUBMITTED_VIA_MAIL = "Application Submitted via Mail"
    CASE_VAB_EMAIL_SENT = "Case submitted to VAB"
    PETITION_SUBMITTED = "Petition Submitted"
    WORKUP_CREATED = "Saved CMA Workup"


class NoteType(db.Model, BaseMixin):
    """
    NoteType class describe a type of note that can be
    There are two main types: Manual & System
    The System type of notes can be:
        - submitted
        - approved
        - rejected
        - paid
    """
    __tablename__ = 'case_note_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    action = db.Column(db.String)

    SUBMITTED = 1
    MANUAL = 2
    APPROVED = 3
    REJECTED = 4
    PAID = 5
    REVIEWED = 6
    UPDATED = 7
    EMAIL_BOUNCED = 8
    FULLY_REJECTED = 9
    REPAIRED = 10
    CREATED = 11
    EMAIL_SENT = 12
    APPROVED_CONTRACT = 13
    WORKUP_CREATED = 14


class RejectReasonSchema(BaseSchema):
    class Meta:
        model = RejectReason


class TagSchema(BaseSchema):
    """
    Case tag model schema
    """

    class Meta:
        model = Tag


class ApplicationTypeSchema(BaseSchema):
    """
    Case owner type model schema
    """

    class Meta:
        model = ApplicationType


class ApplicationSourceSchema(BaseSchema):
    """
    Case application source schema
    """

    class Meta:
        model = ApplicationSource


class ApplicationStatusSchema(BaseSchema):
    """
    Case application status schema
    """

    class Meta:
        model = ApplicationStatus


class MarketingCodeSchema(BaseSchema):
    """
    Case marketing code model schema
    """

    class Meta:
        model = MarketingCode


class CompanyServingSchema(BaseSchema):
    """
    Case company model schema
    """

    class Meta:
        model = CompanyServing


class BaseCasePropertySchema(BaseSchema):
    class Meta:
        model = CaseProperty
    full_address = fields.String(dump_only=True)


class ApplicationNoteSchema(BaseSchema):
    class Meta:
        model = Application
        exclude = ('original_application', 'scan_base64_encoded', 'signature_base64_encoded')

    case_property = Nested(BaseCasePropertySchema(), many=False)


class BaseApplicationSchema(BaseSchema):
    """
    Base application model schema
    """

    class Meta:
        model = Application

    scan_base64_encoded = BytesField(allow_none=True)
    signature_base64_encoded = BytesField(allow_none=True)

    @pre_load
    def adjust_binary_fields(self, data, **kwargs):
        scan = data.get('scan_base64_encoded', None)
        if scan and isinstance(scan, str):
            data['scan_base64_encoded'] = data['scan_base64_encoded'].encode('utf-8')

        signature = data.get('signature_base64_encoded', None)
        if signature and isinstance(signature, str):
            data['signature_base64_encoded'] = data['signature_base64_encoded'].encode('utf-8')

        return data


class NoteTypeSchema(BaseSchema):
    """
    Note type model schema
    """

    class Meta:
        model = NoteType


class NoteSchema(BaseSchema):
    """
    Case note model schema
    """

    class Meta:
        model = Note

    attachment = BytesField(allow_none=True)
    type = Nested("NoteTypeSchema", many=False)
    created_by = Nested("UserSchema", many=False)


class SenderNoteSchema(NoteSchema):
    sender_model = fields.Method("get_sender_model")

    def get_sender_model(self, obj):
        if obj.application:
            return ApplicationNoteSchema().dump(obj.application, many=False)
        elif obj.client:
            return ClientSchema(only=('id', 'full_name')).dump(obj.client, many=False)
        elif obj.case_property:
            return BaseCasePropertySchema().dump(obj.case_property, many=False)
        return None


class TakeoverSchema(BaseSchema):
    """
    Case takeover schema
    """

    class Meta:
        model = Takeover

    application_id = fields.Integer(required=True)


class PaymentTypeSchema(BaseSchema):
    """
    Payment type schema
    """

    class Meta:
        model = PaymentType


class PaymentStatusSchema(BaseSchema):
    """
    Payment status schema
    """

    class Meta:
        model = PaymentStatus


class CaseEmailSchema(BaseSchema):
    class Meta:
        model = CaseEmail


class BillingSchema(BaseSchema):
    class Meta:
        model = Billing

    amount = fields.Float(default=15.0)
    balance = fields.Float(default=0.0)
    attorney_fee = fields.Float(default=0.0)
    late_fee = fields.Float(default=0.0)


class PhysicalApplicationSchema(BaseApplicationSchema):
    """
    Case application model schema with relations
    """

    class Meta:
        model = Application

    email_id = fields.Integer(required=True)
    billing_id = fields.Integer(required=True)

    client = Nested(lambda: ClientSchema(exclude=('applications',)), many=False, dump_only=True)
    company = Nested(CompanyServingSchema(), many=False, dump_only=True)
    application_type = Nested(ApplicationTypeSchema(), many=False, dump_only=True)
    property = Nested(BasePropertyModelSchema(), many=False, dump_only=True)
    source = Nested(ApplicationSourceSchema(), many=False, dump_only=True)
    status = Nested(ApplicationStatusSchema(), many=False, dump_only=True)
    full_name = fields.String(dump_only=True)
    full_address = fields.String(dump_only=True)
    assessment = Nested(AssessmentModelSchema(), many=False, dump_only=True)
    takeovers = Nested(TakeoverSchema(), many=True, dump_only=True)
    payment_status = Nested(PaymentStatusSchema(), many=False, dump_only=True)
    marketing_code = Nested(MarketingCodeSchema(), many=False, dump_only=True)
    payment_type = Nested(PaymentTypeSchema(), many=False, dump_only=True)
    billing = Nested(BillingSchema(), many=False)
    email = Nested(CaseEmailSchema(), many=False)

    @pre_load
    def adjust_fields(self, data, **kwargs):
        """
        Adjust initials, first & last application names
        """
        from app.case_management.services import CaseService

        # make always 'initials' in uppercase
        initials = data.get('initials')
        if initials:
            data['initials'] = initials.upper()

        # make capitalize each word in 'first_name'
        first_name = data.get('first_name')
        if first_name:
            data['first_name'] = CaseService.capitalize_name_words(first_name)

        # make capitalize each word in 'last_name'
        last_name = data.get('last_name')
        if last_name:
            data['last_name'] = CaseService.capitalize_name_words(last_name)

        return data

    # @validates_schema
    # def validate_required(self, data, **kwargs):
    #     property_id = data.get('property_id', None)
    #     if not property_id:
    #         apn = data.get('apn', None)
    #         county = data.get('county', None)
    #
    #         prop = db.session.query(Property).filter_by(apn=apn, county=county).first()
    #         if not prop:
    #             raise ValidationError("Either 'property_id' or 'apn' with 'county' must be specified",
    #                                   'missing_required')


class ApplicationSchema(PhysicalApplicationSchema):
    class Meta:
        model = Application

    first_name = fields.String(allow_none=True, required=False)
    last_name = fields.String(allow_none=True, required=False)


class ApplicationRepairSchema(BaseSchema):
    class Meta:
        model = Application
        fields = (
            'email', 'first_name', 'last_name', 'property_id', 'initials', 'signature_base64_encoded',
            'company_serving', 'application_type', 'payment_type', 'payment_link', 'mailing_line1', 'mailing_line2',
            'mailing_line3', 'mailing_city', 'mailing_state', 'mailing_zip', 'text_updates_1', 'text_updates_2',
            'email_updates', 'marketing_code', 'phone_number_1', 'phone_number_2', 'tax_year', 'repair_token',
            'authorized_signer', 'pin_entered' "email", "first_name", "last_name", "initials", "authorized_signer",
            "text_updates_1", "text_updates_2", "email_updates", "phone_number_1", "phone_number_2",
            "signature_base64_encoded"
        )

    email = fields.String(attribute='email.email_address', dump_only=True)
    first_name = fields.String(attribute='first_name', dump_only=True)
    last_name = fields.String(attribute='last_name', dump_only=True)
    initials = fields.String(attribute='initials', dump_only=True)

    authorized_signer = fields.Integer(attribute='authorized_signer', dump_only=True)
    text_updates_1 = fields.Integer(attribute='sms_alerts_1', dump_only=True)
    text_updates_2 = fields.Integer(attribute='sms_alerts_2', dump_only=True)
    email_updates = fields.Integer(attribute='email.alerts', dump_only=True)

    phone_number_1 = fields.String(attribute='phone_number_1', dump_only=True)
    phone_number_2 = fields.String(attribute='phone_number_2', dump_only=True)
    signature_base64_encoded = fields.String(attribute='signature_base64_encoded', dump_only=True)
    repair_token = fields.String(attribute='repair_token', dump_only=True)

    property_id = fields.Integer(attribute='property_id', dump_only=True)
    company_serving = fields.String(attribute='company.name', dump_only=True)
    application_type = fields.String(attribute='type.name', dump_only=True)
    payment_type = fields.String(attribute='payment_type.name', dump_only=True)
    payment_link = fields.String(attribute='payment_link', dump_only=True)
    mailing_line1 = fields.String(attribute='mailing_line1', dump_only=True)
    mailing_line2 = fields.String(attribute='mailing_line2', dump_only=True)
    mailing_line3 = fields.String(attribute='mailing_line3', dump_only=True)
    mailing_city = fields.String(attribute='mailing_city', dump_only=True)
    mailing_state = fields.String(attribute='mailing_state', dump_only=True)
    mailing_zip = fields.Integer(attribute='mailing_zip', dump_only=True)
    pin_entered = fields.Integer(attribute='pin_entered', dump_only=True)
    marketing_code = fields.String(attribute='marketing_code.name', dump_only=True)
    tax_year = fields.Integer(attribute='tax_year', dump_only=True)


class PublicApplicationSchema(BaseApplicationSchema):
    email = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    property_id = fields.Integer(required=True)
    initials = fields.String(default='')
    company_serving = fields.String(required=True)
    application_type = fields.String(required=True)
    payment_type = fields.String()
    payment_link = fields.String()

    # mailing address fields
    mailing_line1 = fields.String(allow_none=True)
    mailing_line2 = fields.String(allow_none=True)
    mailing_line3 = fields.String(allow_none=True)
    mailing_city = fields.String(allow_none=True)
    mailing_state = fields.String(allow_none=True)
    mailing_zip = fields.Integer(allow_none=True)

    authorized_signer = fields.Integer(required=True)
    email_updates = fields.Integer()
    text_updates_1 = fields.Integer()
    text_updates_2 = fields.Integer()
    pin_entered = fields.Integer()
    marketing_code = fields.String(default='')
    phone_number_1 = fields.String(required=True)
    phone_number_2 = fields.String(allow_none=True)
    tax_year = fields.Integer(required=True)
    # scan_base64_encoded = BytesField()
    signature_base64_encoded = BytesField(required=True)

    MAX_SUBMISSION_COUNT = 10

    def white_signature(self, signature_encoded, amount=50):
        try:

            img = Image.open(BytesIO(base64.b64decode(signature_encoded)))

            # not white pixels counter
            pixels = 0
            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    px = img.getpixel((i, j))
                    if px[0] == 255 and px[1] == 255 and px[2] == 255:
                        continue
                    else:
                        pixels += 1
                        if pixels > amount:
                            return False
            return True
        except Exception as e:
            raise ValidationError(e.args[0], 'signature_base64_encoded')

    # @validates_schema
    # def validate_owner_first_last_names(self, data, **kwargs):
    #
    #     first_name = data['first_name']
    #     last_name = data['last_name']
    #     property_id = data['property_id']
    #
    #     from app.routing.services import PropertyService
    #     owner = PropertyService.get_matched_owner(property_id, first_name, last_name)
    #
    #     if not owner:
    #         raise ValidationError("Owner does not match", "owner_mismatch")

    # @validates_schema
    # def validate_application_duplication(self, data, **kwargs):
    #
    #     tax_year = data.get('tax_year')
    #     prop = db.session.query(Property).filter_by(id=data.get('property_id')).first()
    #
    #     if Application.exists(property_id=prop.id, tax_year=tax_year):
    #         raise ValidationError(
    #             "An application was already submitted for this property. Please give us a call at 305-504-5094 "
    #             "if there was an error in your previous submission.", 'duplicate'
    #         )

    @validates_schema
    def validate_max_submission_count(self, data, **kwargs):
        property_id = data['property_id']

        today_apps = db.session.query(Application).filter(
            Application.property_id == property_id,
            (Application.created_at + timedelta(days=1)) > datetime.now()
        ).all()
        if len(today_apps) > self.MAX_SUBMISSION_COUNT:
            raise ValidationError(
                "Reached today's limit of {} application submissions for the property_id={}".format(
                    self.MAX_SUBMISSION_COUNT, property_id
                ),
                "max_submission"
            )

    # @validates('payment_type')
    # def validate_payment_type(self, value):
    #     payment_types = [o.name for o in db.session.query(PaymentType.name).distinct()]
    #     if value not in payment_types:
    #         raise ValidationError('Invalid payment type', 'payment_type')

    @validates('marketing_code')
    def validate_marketing_code(self, value):
        codes = [o.name for o in db.session.query(MarketingCode.name).distinct()]
        if value not in codes:
            raise ValidationError('Invalid marketing code', 'marketing_code')

    @validates('signature_base64_encoded')
    def validate_signature_base64_encoded(self, value):
        # file_path = DATA_IMPORT / 'signature_white.png'
        # with open(file_path, "rb") as image_file:
        #     encoded_string = base64.b64encode(image_file.read())
        #     print(encoded_string)

        if self.white_signature(value):
            raise ValidationError('Invalid signature', 'signature_base64_encoded')

    @validates('email_updates')
    def validate_email_updates(self, value):
        if value not in (0, 1):
            raise ValidationError("Invalid value, can be 0 or 1", "email_updates")

    @validates('text_updates_1')
    def validate_text_updates_1(self, value):
        if value not in (0, 1):
            raise ValidationError("Invalid value, can be 0 or 1", "text_updates")

    @validates('text_updates_2')
    def validate_text_updates_2(self, value):
        if value not in (0, 1):
            raise ValidationError("Invalid value, can be 0 or 1", "text_updates")

    @validates('authorized_signer')
    def validate_authorized_signer(self, value):
        if value == 0:
            raise ValidationError("Not authorized signer", "authorized_signer")
        elif value != 1:
            raise ValidationError("Invalid value", "authorized_signer")

    @validates('pin_entered')
    def validate_pin_entered(self, value):
        if value not in (0, 1):
            raise ValidationError("Invalid value, can be 0 or 1", "pin_entered")

    @validates('company_serving')
    def validate_company_serving(self, value):
        companies = [o.name for o in db.session.query(CompanyServing.name).distinct()]
        if value not in companies:
            raise ValidationError('Invalid company name', 'company_serving')

    @validates('application_type')
    def validate_application_type(self, value):
        app_types = [o.name for o in db.session.query(ApplicationType.name).distinct()]
        if value not in app_types:
            raise ValidationError('Invalid application type name', 'application_type')

    @validates('property_id')
    def validate_property_id(self, value):
        if not value:
            raise ValidationError('Missing required param', 'property_id')

        prop = db.session.query(Property).filter_by(id=value).first()
        if not prop:
            raise ValidationError('Property with id={} was not found'.format(value), 'property_id')


class ClientTypeSchema(BaseSchema):
    class Meta:
        model = ClientType


class CasePropertyStatusSchema(BaseSchema):
    class Meta:
        model = CasePropertyStatus


class CasePropertySchema(BaseSchema):
    """
    Case property model schema
    """

    class Meta:
        model = CaseProperty

    from app.singlecma.models import SingleCMAWorkupsSchema

    workups = Nested(SingleCMAWorkupsSchema(exclude=('cma_payload', )), many=True, dump_only=True)
    status = Nested(CasePropertyStatusSchema(), many=False)
    full_address = fields.String(dump_only=True)
    payment_status = Nested(PaymentStatusSchema(), many=False, dump_only=True)
    payment_type = Nested(PaymentTypeSchema(), many=False, dump_only=True)
    property = Nested(BasePropertyModelSchema(), many=False, dump_only=True)
    application = Nested(ApplicationSchema(
        exclude=('client', 'original_application', 'scan_base64_encoded', 'signature_base64_encoded')),
        many=False,
        dump_only=True
    )
    client = Nested(
        lambda: ClientSchema(
            exclude=(
                'applications', 'case_properties', 'email', 'type', 'tags', 'company_serving'
            )
        ),
        many=False,
        dump_only=True
    )
    assessment = Nested(AssessmentModelSchema(), many=False)


class ClientSchema(BaseSchema):
    """
    Case client model schema
    """

    class Meta:
        model = Client

    company_serving = Nested(CompanyServingSchema(), many=False)
    applications = Nested(ApplicationSchema(
        exclude=('client', 'original_application', 'scan_base64_encoded', 'signature_base64_encoded')),
        many=True
    )
    case_properties = Nested(CasePropertySchema(exclude=('client', 'application', 'property')), many=True)
    tags = Nested(TagSchema(), many=True)
    type = Nested(ClientTypeSchema(), many=False)
    full_name = fields.String(dump_only=True)
    email = Nested(CaseEmailSchema(), many=False)
