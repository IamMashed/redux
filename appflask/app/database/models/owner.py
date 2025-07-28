from datetime import datetime

from marshmallow import Schema, fields
from sqlalchemy import CheckConstraint

from app import db
from app.case_management.types import FullName
from app.database.models.mixin import UpsertMixin, ValidationMixin
from app.settings.models import BaseSchema


class Owner(db.Model, UpsertMixin):
    # TODO: fixme, more than one records can be stored in table for the same property_id & data_source
    id = db.Column(db.Integer(), primary_key=True)
    data_source = db.Column(db.String(), nullable=False)
    property_id = db.Column(
        db.Integer,
        db.ForeignKey('property.id', name='owner_property_id_fkey', ondelete='cascade'),
        nullable=False,
        index=True,
        onupdate='CASCADE'
    )
    created_on = db.Column(db.Date, default=datetime.today())
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    street_address = db.Column(db.String)
    second_owner_first_name = db.Column(db.String)
    second_owner_last_name = db.Column(db.String)

    owner_address_1 = db.Column(db.String)
    owner_address_2 = db.Column(db.String)
    owner_address_3 = db.Column(db.String)

    owner_city = db.Column(db.String)
    owner_state = db.Column(db.String)
    owner_zip = db.Column(db.Integer)

    first_full_name = db.composite(FullName, first_name, last_name)
    second_full_name = db.composite(FullName, second_owner_first_name, second_owner_last_name)

    matching = db.Column(db.Boolean)

    __table_args_ = (
        CheckConstraint("owner.data_source IN ('sale', 'property', 'assessment')")
    )

    def get_full_names(self):
        full_names = []
        for full_name in [self.first_full_name, self.second_full_name]:
            if full_name and str(full_name) and full_name not in full_names:
                full_names.append(full_name)
        return full_names


class OwnerValidation(db.Model, ValidationMixin):
    id = db.Column(db.Integer, primary_key=True)
    apn = db.Column(db.String)
    county = db.Column(db.String)
    errors = db.Column(db.JSON)


class OwnerSchema(Schema):
    apn = fields.String(data_key='apn', required=True)
    county = fields.String(data_key='county', required=True)
    data_source = fields.String(data_key='data_source', required=True)

    created_on = fields.Date(data_key='created_on', missing='2000-01-01')
    first_name = fields.String(data_key='own_first_name', missing=None)
    last_name = fields.String(data_key='own_last_name', missing=None)

    second_owner_first_name = fields.String(data_key='own_second_owner_first_name', missing=None)
    second_owner_last_name = fields.String(data_key='own_second_owner_last_name', missing=None)

    owner_address_1 = fields.String(data_key='own_address_1', missing=None)
    owner_address_2 = fields.String(data_key='own_address_2', missing=None)
    owner_address_3 = fields.String(data_key='own_address_3', missing=None)

    owner_city = fields.String(data_key='own_city', missing=None)
    owner_state = fields.String(data_key='own_state', missing=None)
    owner_zip = fields.Integer(data_key='own_zip', allow_none=True, missing=None)


class OwnerModelSchema(BaseSchema):
    class Meta:
        model = Owner
