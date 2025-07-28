from abc import abstractmethod
from datetime import datetime

from deepdiff import DeepDiff
from flask_login import current_user
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.exceptions import abort

from app import db
from .types import FullMailingAddress


class StateChangedMixin(object):

    exclude_paths = {
        "root['property']", "root['signature_base64_encoded']", "root['scan_base64_encoded']",
        "root['client']", "root['updated_at']", "root['created_at']", "root['applications']",
        "root['notes']", "root['original_application']", "root['marketing_code']",
        "root['payment_type']", "root['status']", "root['case_properties']", "root['email_id']",
        "root['application']['signature_base64_encoded']", "root['payment_status']", "root['application']",
        "root['updated_by_id']", "root['repair_token']", "root['full_name']", "root['email']['id']",
        "root['email']['confirm_token']", "root['email']['originated_from_id']"
    }

    @classmethod
    def parse_key(cls, key):
        idx = key.rfind('[')
        return key[idx + 2: -2]

    @classmethod
    def get_field_value(cls, model, value, attribute):
        if value:
            obj = model.get(value)

            if obj and hasattr(obj, attribute):
                return getattr(obj, attribute)
        return None

    @classmethod
    def get_field_text(cls, field_name, old_value, new_value):
        if old_value is not None and new_value is not None:
            return f" Changed {field_name} from {old_value} to {new_value}."
        elif new_value:
            return f" Changed {field_name} to {new_value}."
        else:
            return f" Changed {field_name} from {old_value} to ''."

    @classmethod
    def valid_values(cls, old_value, new_value):
        if old_value or new_value:
            return True
        return False

    @classmethod
    def get_changes_text(cls, changes):
        if changes is None:
            return '', []
        text = ''
        fields_changed = []
        for key in changes.keys():
            old_value = changes[key]['old_value']
            new_value = changes[key]['new_value']

            if not cls.valid_values(old_value, new_value):
                continue

            field_mapper = cls.get_fields_mapper(key)
            if field_mapper:
                field_name, old_value, new_value = cls._get_mapper_values(field_mapper, old_value, new_value)
            else:
                field_name = cls.parse_key(key)
            if old_value or new_value:
                text = text + cls.get_field_text(field_name, old_value, new_value)
                fields_changed.append(field_name)
        return text, fields_changed

    @classmethod
    def _get_mapper_values(cls, mapper, old_value, new_value):
        model = mapper.get('model')
        attribute = mapper.get('attribute')
        field_name = mapper.get('field')

        old_value = cls.get_field_value(model, old_value, attribute)
        new_value = cls.get_field_value(model, new_value, attribute)

        return field_name, old_value, new_value

    @classmethod
    def email_changed(cls, fields):
        if 'email_address' in fields:
            return True
        return False

    @classmethod
    def get_state_changes_text(cls, current, target, **kwargs):

        # get the difference to see what was modified
        # paths = kwargs.get('exclude_paths').copy() if kwargs.get('exclude_paths') else set()

        if kwargs.get('exclude_paths'):
            kwargs['exclude_paths'] = kwargs['exclude_paths'].update(StateChangedMixin.exclude_paths)
        else:
            kwargs['exclude_paths'] = StateChangedMixin.exclude_paths

        diff = DeepDiff(current, target, ignore_numeric_type_changes=True, **kwargs)
        values_changed = diff.get('values_changed')
        type_changes = diff.get('type_changes')

        values_changed_text, value_fields = cls.get_changes_text(values_changed)
        type_changes_text, type_fields = cls.get_changes_text(type_changes)

        text = values_changed_text + type_changes_text
        fields = value_fields + type_fields

        return text, fields

    @abstractmethod
    def get_fields_mapper(cls, key) -> dict:
        pass


class BaseMixin(object):
    _repr_hide = ['created_at', 'updated_at']

    @classmethod
    def query(cls):
        return db.session.query(cls)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_or_404(cls, id):
        rv = cls.get(id)
        if rv is None:
            abort(404)
        return rv

    @classmethod
    def get_or_create(cls, **kwargs):
        r = cls.get_by(**kwargs)
        if not r:
            r = cls(**kwargs)
            db.session.add(r)

        return r

    @classmethod
    def create(cls, **kwargs):
        r = cls(**kwargs)
        db.session.add(r)
        return r

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in self.__table__.c.keys() if n not in self._repr_hide)
        return "{}({})".format(self.__class__.__name__, values)


class ApplicationCasePropertyMixin(object):
    """
    Common attributes of 'application' and 'case property'
    """

    @declared_attr
    def company_id(cls):
        """
        Reference to 'CompanyServing'
        """
        return db.Column(
            db.Integer,
            db.ForeignKey(
                "case_company_serving.id", name="fk_{}_company_id".format(cls.__name__), onupdate='CASCADE'
            ),
            nullable=True,
        )

    @declared_attr
    def property_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey(
                "property.id", name="fk_{}_property_id".format(cls.__name__), onupdate='CASCADE'
            ),
            nullable=True,
        )

    @declared_attr
    def property(cls):
        return db.relationship('Property', uselist=False)

    @declared_attr
    def pin_code(cls):
        return db.Column(db.String)

    @declared_attr
    def address_line1(cls):
        """
        Physical address line 1
        """
        return db.Column(db.String)

    @declared_attr
    def address_line2(cls):
        """
        Physical address line 2
        """
        return db.Column(db.String)

    @declared_attr
    def address_city(cls):
        """
        Physical address city
        """
        return db.Column(db.String)

    @declared_attr
    def address_state(cls):
        """
        Physical address state
        """
        return db.Column(db.String)

    @declared_attr
    def address_zip(cls):
        """
        Physical address zip
        """
        return db.Column(db.Integer)

    @declared_attr
    def tax_year(cls):
        """
        Tax year
        """
        return db.Column(db.Integer)

    @declared_attr
    def apn(cls):
        """
        Property APN
        """
        return db.Column(db.String)

    @declared_attr
    def county(cls):
        """
        Property county
        """
        return db.Column(db.String)

    @declared_attr
    def payment_type_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey(
                'case_payment_type.id', name="fk_{}_payment_type_id".format(cls.__name__), onupdate='CASCADE'
            ),
            nullable=True,
        )

    @declared_attr
    def payment_type(cls):
        return db.relationship('PaymentType', uselist=False)

    @declared_attr
    def payment_status_id(cls):
        from .models import PaymentStatus
        return db.Column(
            db.Integer,
            db.ForeignKey(
                'case_payment_status.id', name="fk_{}_payment_status_id".format(cls.__name__), onupdate='CASCADE'
            ),
            default=PaymentStatus.UNPAID,
        )

    @declared_attr
    def payment_status(cls):
        return db.relationship('PaymentStatus', uselist=False)

    @hybrid_property
    def full_address(self):
        """
        Full property address instance level
        """

        address_line1 = self.address_line1 or ''
        address_line2 = self.address_line2 or ''
        address_city = self.address_city or ''
        address_state = self.address_state or ''
        address_zip = self.address_zip or ''

        full_address = ' '.join([address_line1, address_line2, address_city, address_state, str(address_zip)])

        # full_address = FullAddress(self.address_line1, self.address_line2, self.address_city,
        #                            self.address_state, self.address_zip)
        # return full_address.__repr__()
        return full_address

    @full_address.expression
    def full_address(cls):
        """
        Full property address class level expression
        """
        address_line1 = cls.address_line1 or ''
        address_line2 = cls.address_line2 or ''
        address_city = cls.address_city or ''
        address_state = cls.address_state or ''
        address_zip = cls.address_zip or ''

        return db.func.concat(address_line1, ' ', address_line2, ' ', address_city, ' ',
                              address_state, ' ', address_zip)


class ApplicationClientMixin(object):
    """
    Common attributes of 'application' and 'client'
    """

    @declared_attr
    def first_name(cls):
        """
        First name of a user
        """
        return db.Column(db.String)

    @declared_attr
    def last_name(cls):
        """
        Last name of a user
        """
        return db.Column(db.String)

    @hybrid_property
    def full_name(self):
        """
        Full name instance level
        """
        first_name = self.first_name or ''
        last_name = self.last_name or ''

        return (first_name + ' ' + last_name).strip()

    @full_name.expression
    def full_name(cls):
        """
        Full name class level expression to used in queries
        """
        first_name = cls.first_name or ''
        last_name = cls.last_name or ''

        return db.func.concat(first_name, ' ', last_name)

    @declared_attr
    def mailing_line1(cls):
        """
        Mailing address line 1
        """
        return db.Column(db.String)

    @declared_attr
    def mailing_line2(cls):
        """
        Mailing address line 2
        """
        return db.Column(db.String)

    @declared_attr
    def mailing_line3(cls):
        """
        Mailing address line 3
        """
        return db.Column(db.String)

    @declared_attr
    def mailing_city(cls):
        """
        Mailing address city
        """
        return db.Column(db.String)

    @declared_attr
    def mailing_state(cls):
        """
        Mailing address state
        """
        return db.Column(db.String)

    @declared_attr
    def mailing_zip(cls):
        """
        Mailing address zip
        """
        return db.Column(db.Integer)

    @hybrid_property
    def full_mailing_address(self):
        """
        Full mailing address instance level
        """

        address = FullMailingAddress(self.mailing_line1, self.mailing_line2, self.mailing_line3)
        return address.__repr__()

    @declared_attr
    def phone_number_1(cls):
        """
        First phone number
        """
        return db.Column(db.String)

    @declared_attr
    def phone_number_2(cls):
        """
        Second phone number
        """
        return db.Column(db.String)

    @declared_attr
    def sms_alerts_1(cls):
        """
        Whether send sms alerts on phone_number_1
        """
        return db.Column(db.Boolean, default=True)

    @declared_attr
    def sms_alerts_2(cls):
        """
        Whether send sms alerts on phone_number_2
        """
        return db.Column(db.Boolean, default=False)

    @declared_attr
    def marketing_code_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey(
                'case_marketing_code.id', name="fk_{}_case_marketing_code_id".format(cls.__name__), onupdate='CASCADE'
            ),
            nullable=True,
        )

    @declared_attr
    def marketing_code(cls):
        return db.relationship('MarketingCode', uselist=False)

    @declared_attr
    def email_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey(
                'case_email.id', name="fk_{}_email_id".format(cls.__name__), onupdate='CASCADE'
            ),
            nullable=True,
        )

    @declared_attr
    def email(cls):
        return db.relationship('CaseEmail', uselist=False)

    @declared_attr
    def billing_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey(
                "case_billing.id", name="fk_{}_billing_id".format(cls.__name__), onupdate='CASCADE', ondelete="CASCADE"
            ),
            nullable=True,
        )

    @declared_attr
    def billing(cls):
        return db.relationship('Billing', cascade="all,delete", uselist=False)


class AuditMixin(object):
    fields = ('updated_at', 'created_at', 'created_by_id', 'updated_by_id')

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @declared_attr
    def created_by_id(cls):
        """
         ID of the user who create the entry
        """
        return db.Column(
            db.Integer,
            db.ForeignKey('users.id', name='fk_{}_created_by_id'.format(cls.__name__), use_alter=True),
            # nullable=False,
            default=cls.current_user_id_or_none
        )

    @declared_attr
    def created_by(cls):
        """
        Relation to user, who create the entry
        """
        return db.relationship(
            'User',
            # primaryjoin=lambda: User.id == cls.created_by_id,
            primaryjoin='User.id == {}.created_by_id'.format(cls.__name__),
            remote_side='User.id'
        )

    @declared_attr
    def updated_by_id(cls):
        """
        ID of the user who update the entry
        """
        return db.Column(
            db.Integer,
            db.ForeignKey('users.id', name='fk_{}_updated_by_id'.format(cls.__name__), use_alter=True),
            # nullable=False,
            default=cls.current_user_id_or_none,
            onupdate=cls.current_user_id_or_none
        )

    @declared_attr
    def updated_by(cls):
        """
        Relation to user, who update the entry
        """
        return db.relationship(
            'User',
            primaryjoin='User.id == {}.updated_by_id'.format(cls.__name__),
            remote_side='User.id'
        )

    @classmethod
    def current_user_id_or_none(cls):
        try:
            return current_user.id
        except Exception as e:
            print(e.args)
            return None
