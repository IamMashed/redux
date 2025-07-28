from marshmallow import fields, validate, pre_load, Schema
from app import db
from app.database.models.mixin import UpsertMixin, ValidationMixin
from app.settings.models import BaseSchema


class Sale(db.Model, UpsertMixin):
    id = db.Column(db.Integer(), primary_key=True)

    property_id = db.Column(
        db.Integer,
        db.ForeignKey('property.id', name='sale_property_id_fkey', ondelete='cascade'),
        nullable=False,
        onupdate='CASCADE',
        index=True
    )

    # A key component for algorithms
    price = db.Column(db.Integer(), index=True)

    # Filtering by
    date = db.Column(db.Date(), index=True)

    # Possibility to Filter out Arms Length sales from the algorithm
    arms_length = db.Column(db.Boolean(), index=True)

    seller_first_name = db.Column(db.String, nullable=True)
    seller_last_name = db.Column(db.String, nullable=True)

    buyer_first_name = db.Column(db.String, nullable=True)
    buyer_last_name = db.Column(db.String, nullable=True)


class SaleValidation(db.Model, ValidationMixin):
    id = db.Column(db.Integer, primary_key=True)
    apn = db.Column(db.String)
    county = db.Column(db.String)
    errors = db.Column(db.JSON)


class SaleSchema(Schema):
    """
    Schema will be used to validate sale data before storning to database
    """
    apn = fields.String(required=True, data_key='print_key')
    county = fields.String(
        required=True,
        validate=validate.Length(min=1,
                                 error='county should not be empty')
    )
    swis_code = fields.String(data_key='swis_code')
    price = fields.Integer(data_key='sale_price')
    date = fields.Date(data_key='sale_date')
    arms_length = fields.Boolean()

    seller_first_name = fields.String(data_key="seller_first_name")
    seller_last_name = fields.String(data_key="seller_last_name")
    # owner information
    owner_first_name = fields.String(data_key='buyer_first_name')
    owner_last_name = fields.String(data_key='buyer_last_name')
    owner_address = fields.String()
    second_owner_last_name = fields.String(data_key='buyer_last_name2')

    @pre_load
    def adjust_arms_length(self, data, **kwargs):
        data['arms_length'] = True \
            if data['arms_length_flag'] == 'Y' else False
        data['county'] = data['county_name'].lower()

        data['owner_address'] = ','.join([data['buyer_street_name'], data['buyer_street_nbr'],
                                          data['buyer_city'], data['buyer_state'],
                                          data['buyer_zip5'], data['buyer_zip4']])
        return data


class NassauSaleSchema(SaleSchema):
    apn = fields.String(required=True)

    @pre_load
    def adjust_apn(self, data, **kwargs):
        """
        7.-231-18 ==> 07231  00180
        7.-142-242 ==> 07142  02420
        """
        numbers = data['print_key'].split('-')
        first = numbers[0].replace('.', '').zfill(2)
        second = numbers[1]
        if second.isdigit():
            second = numbers[1].zfill(3)
        else:
            second = numbers[1].rjust(3)
        third = numbers[2].zfill(4)
        data['apn'] = ''.join(
            [first, second, '  ', third, '0']).replace('.', '')
        return data


class BaseSaleSchema(Schema):
    apn = fields.String(data_key='apn', required=True)
    county = fields.String(required=True, validate=validate.Length(min=1, error='county should not be empty'))
    price = fields.Float(data_key='price', missing=None)
    date = fields.Date(data_key='date', missing=None)
    arms_length = fields.Boolean(data_key='arms_length', missing=None)

    seller_first_name = fields.String(data_key="seller_first_name", missing=None)
    seller_last_name = fields.String(data_key="seller_last_name", missing=None)

    buyer_first_name = fields.String(data_key='buyer_first_name', missing=None)
    buyer_last_name = fields.String(data_key='buyer_last_name', missing=None)


class SaleModelSchema(BaseSchema):
    class Meta:
        model = Sale
