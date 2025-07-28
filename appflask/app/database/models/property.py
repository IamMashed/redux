from datetime import date

from geoalchemy2 import Geometry
from dataclasses import dataclass
import marshmallow_dataclass
from marshmallow import fields, pre_load, Schema
from marshmallow.fields import Nested
from sqlalchemy import ARRAY, Integer, Index, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app import db
from app.database.models.mixin import ValidationMixin, UpsertMixin
from app.settings.models import BaseSchema
from app.utils.constants import BASEMENT_TYPE_MAP, County, MIAMIDADE_CONDO_CODES, PROPERTY_CLASS_DESCRIPTION_MAP

NASSAU_VILLAGE_CODES = [
    'OB', 'KP', 'FPS', 'CED', 'PN', 'KE', 'FPT', 'HN', 'MH', 'CN', 'UB', 'GE', 'CI', 'PL',
    'RVC', 'HH', 'EW', 'NHP', 'RH', 'MI', 'BRO', 'EH', 'MP', 'LYN', 'LH', 'HEM', 'SC', 'SM',
    'GC', 'BLR', 'FM', 'GLC', 'NH', 'AB', 'LT',
    'RG', 'MU', 'SR', 'MAL', 'RO', 'FP', 'PH', 'ER', 'SU', 'MN', 'SP', 'RE', 'LB',
    'WBG', 'HBP', 'GN', 'OW', 'WE',
    'TH', 'GP', 'OC', 'WP', 'MK', 'VS', 'BE', 'LAW', 'BAY', 'IP', 'PM', 'FH'
]

NASSAU_PROPERTY_STYLES = [
    ('1', 'RANCH'),
    ('2', 'RAISED RANCH/HI RANCH'),
    ('3', 'SPLIT LEVEL'),
    ('4', 'MODIFIED RANCH'),
    ('5', 'CAPE'),
    ('6', 'COLONIAL'),
    ('7', 'VICTORIAN'),
    ('8', 'CONTEMPORARY'),
    ('9', 'OLD STYLE'),
    ('10', 'BUNGALOW,COTTAGE'),
    ('11', 'DUPLEX OR TRIPLEX'),
    ('12', 'MANSION, ESTATE'),
    ('13', 'TOWNHOUSE'),
    ('14', 'CONDO'),
    ('15', 'CO-OP'),
    ('16', 'HOMOWNER ASSOC'),
    ('17', 'OTHER'),
    ('18', 'SPLANCH'),
    ('19', 'CARRIAGE HOUSE'),
    ('20', 'Tudor'),
    ('21', 'Store/Dwell')
]

NASSAU_HEAT_CODES = [
    ('1', 'NONE'),
    ('2', 'NON-CNTRL'),
    ('3', 'CNTRL HEAT'),
    ('4', 'CNTRL HTAC')
]

TOWNS = {
    'nassau': {
        '1': 'Hempstead',
        '2': 'North Hempstead',
        '3': 'Oyster Bay',
        '4': 'Glen Cove',
        '5': 'Long Beach'
    },
    'suffolk': {
        '100': 'Babylon',
        '200': 'Brookhaven',
        '300': 'East Hampton',
        '400': 'Hungtington',
        '500': 'Islip',
        '600': 'Riverhead',
        '700': 'Shelter Island',
        '800': 'Smithtown',
        '900': 'Southampton',
        '1000': 'Southold'
    },
    'broward': {'OAKLAND PARK': 'OAKLAND PARK', 'COOPER CITY': 'COOPER CITY',
                'SEA RANCH LAKES': 'SEA RANCH LAKES', 'DEERFIELD BEACH': 'DEERFIELD BEACH',
                'LAUD BY THE SEA': 'LAUD BY THE SEA', 'WESTON': 'WESTON', 'PARKLAND': 'PARKLAND',
                'DAVIE': 'DAVIE', 'DANIA BEACH': 'DANIA BEACH', 'PEMBROKE PINES': 'PEMBROKE PINES',
                'POMPANO BEACH': 'POMPANO BEACH', 'WEST PARK': 'WEST PARK', 'TAMARAC': 'TAMARAC',
                'MIRAMAR': 'MIRAMAR', 'LAZY LAKE': 'LAZY LAKE', 'HALLANDALE BEACH': 'HALLANDALE BEACH',
                'COCONUT CREEK': 'COCONUT CREEK', 'MARGATE': 'MARGATE',
                'LAUDERDALE LAKES': 'LAUDERDALE LAKES', 'CORAL SPRINGS': 'CORAL SPRINGS',
                'WILTON MANORS': 'WILTON MANORS', 'UNINCORPORATED': 'UNINCORPORATED',
                'FORT LAUDERDALE': 'FORT LAUDERDALE', 'SUNRISE': 'SUNRISE',
                'LAUDERHILL': 'LAUDERHILL', 'PLANTATION': 'PLANTATION', 'HOLLYWOOD': 'HOLLYWOOD',
                'LIGHTHOUSE POINT': 'LIGHTHOUSE POINT', 'PEMBROKE PARK': 'PEMBROKE PARK',
                'SOUTHWEST RANCHES': 'SOUTHWEST RANCHES', 'HILLSBORO BEACH': 'HILLSBORO BEACH',
                'NORTH LAUDERDALE': 'NORTH LAUDERDALE'},
    'miamidade': {'Medley': 'Medley', 'Hialeah Gardens': 'Hialeah Gardens',
                  'Sunny Isles Beach': 'Sunny Isles Beach', 'Key Biscayne': 'Key Biscayne',
                  'Indian Creek': 'Indian Creek', 'North Bay Village': 'North Bay Village',
                  'Golden Beach': 'Golden Beach', 'North Miami Beach': 'North Miami Beach',
                  'Miami Gardens': 'Miami Gardens', 'South Miami': 'South Miami',
                  'Miami Springs': 'Miami Springs', 'Palmetto Bay': 'Palmetto Bay',
                  'Aventura': 'Aventura', 'Doral': 'Doral', 'Sweetwater': 'Sweetwater',
                  'Miami Beach': 'Miami Beach', 'Bal Harbour': 'Bal Harbour',
                  'Virginia Gardens': 'Virginia Gardens', 'North Miami': 'North Miami',
                  'Biscayne Park': 'Biscayne Park', 'Pinecrest': 'Pinecrest',
                  'Opa-locka': 'Opa-locka', 'El Portal': 'El Portal',
                  'Coral Gables': 'Coral Gables', 'Miami Shores': 'Miami Shores',
                  'Bay Harbor Islands': 'Bay Harbor Islands', 'Hialeah': 'Hialeah',
                  'West Miami': 'West Miami', 'Miami Lakes': 'Miami Lakes', 'Homestead': 'Homestead',
                  'Florida City': 'Florida City', 'Unincorporated County': 'Unincorporated County',
                  'Surfside': 'Surfside', 'Cutler Bay': 'Cutler Bay', 'Miami': 'Miami'},
    'palmbeach': {
        '2': 'Atlantis',
        '4': 'Belle Glade',
        '6': 'Boca Raton',
        '8': 'Boynton Beach',
        '9': 'Briny Breezes',
        '10': 'Cloud Lake',
        '12': 'Delray Beach',
        '14': 'Glen Ridge',
        '18': 'Greenacres',
        '20': 'Gulf Stream',
        '22': 'Haverhill',
        '24': 'Highland Beach',
        '26': 'Hypoluxo',
        '28': 'Juno Beach',
        '30': 'Jupiter',
        '32': 'Jupiter Inlet Colony',
        '34': 'Lake Clarke Shores',
        '36': 'Lake Park',
        '38': 'Lake Worth',
        '40': 'Lantana',
        '41': 'Loxahatchee Groves',
        '42': 'Manalapan',
        '44': 'Mangonia Park',
        '46': 'Ocean Ridge',
        '48': 'Pahokee',
        '50': 'Palm Beach',
        '52': 'Palm Beach Gardens',
        '54': 'Palm Beach Shores',
        '56': 'Riviera Beach',
        '58': 'South Bay',
        '60': 'Tequesta',
        '62': 'South Palm Beach',
        '66': 'Village of Golf',
        '68': 'North Palm Beach',
        '70': 'Palm Springs',
        '72': 'Royal Palm Beach',
        '73': 'Wellington',
        '74': 'West Palm Beach',
        '77': 'Westlake',
        '00': '00'}  # TODO: define the zero
}


class PropertyCounty(db.Model):
    __tablename__ = 'property_county'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    number = db.Column(db.Integer)


class AbstractProperty(db.Model):
    __abstract__ = True

    @declared_attr
    def __table_args__(cls):
        return (
            Index('ix_{}_number'.format(cls.__name__), 'number'),
            Index('ix_{}_school_district'.format(cls.__name__), 'school_district'),
            Index('ix_{}_state'.format(cls.__name__), 'state'),
            Index('ix_{}_street'.format(cls.__name__), 'street'),
            Index('ix_{}_town'.format(cls.__name__), 'town'),
            Index('ix_{}_village'.format(cls.__name__), 'village'),
            Index('ix_{}_zip'.format(cls.__name__), 'zip'),
            Index('ix_{}_section'.format(cls.__name__), 'section'),
            Index('ix_{}_block'.format(cls.__name__), 'block'),
            Index('ix_{}_undefined_field'.format(cls.__name__), 'undefined_field'),
            Index('ix_{}_print_key'.format(cls.__name__), 'print_key'),
            Index('ix_{}_lot'.format(cls.__name__), 'lot'),
            Index('ix_{}_is_residential'.format(cls.__name__), 'is_residential'),
            Index('ix_{}_address'.format(cls.__name__), 'address'),
            db.UniqueConstraint('apn', 'county', name='uc_{}_apn_county'.format(cls.__name__)),
        )

    @declared_attr
    def county(cls):
        return db.Column(
            db.String,
            db.ForeignKey(
                "property_county.id", name="fk_{}_property_county_id".format(cls.__name__), onupdate='CASCADE'
            ),
            nullable=False,
        )

    @declared_attr
    def property_county(cls):
        return db.relationship('PropertyCounty', uselist=False)

    @declared_attr
    def reference_building(cls):
        return db.Column(Integer, ForeignKey('property.id'), nullable=True)

    id = db.Column(db.Integer(), primary_key=True)

    # house identity number
    # APN, or a combination of District + Section + Block + Lot
    # a.k.a PARID ending with 0
    apn = db.Column(db.String(), nullable=False)
    # county = db.Column(db.String(), nullable=False)
    school_district = db.Column(db.Integer())
    district = db.Column(db.String())
    section = db.Column(db.String())
    block = db.Column(db.String())
    undefined_field = db.Column(db.String)
    print_key = db.Column(db.String)
    lot = db.Column(db.String())

    village = db.Column(db.String)
    address = db.Column(db.String())

    #  "Legal Description" is required to submit the forms within two days
    legal = db.Column(db.String)

    # IT will go into Single CMA web and print versions
    subdivision = db.Column(db.String)

    street = db.Column(db.String())
    number = db.Column(db.String())  # house number
    town = db.Column(db.String(length=255))
    state = db.Column(db.String())
    zip = db.Column(db.Integer)
    city = db.Column(db.String)

    latitude = db.Column(db.Float(), index=True)
    longitude = db.Column(db.Float(), index=True)
    coordinate_x = db.Column(db.Float())
    coordinate_y = db.Column(db.Float())
    geo = db.Column(Geometry(geometry_type="POINT"))

    is_condo = db.Column(db.Boolean(), index=True)
    is_listed = db.Column(db.Boolean())

    property_class = db.Column(db.Integer)
    property_class_type = db.Column(db.Integer)
    building_code = db.Column(db.Integer)
    data_composite = db.Column(ARRAY(Integer))
    age = db.Column(db.Integer)
    effective_age = db.Column(db.Integer)

    hamlet = db.Column(db.String)
    gla_sqft = db.Column(db.Float)
    under_air_gla_sqft = db.Column(db.Float)
    waterfront = db.Column(db.Boolean)
    rooms = db.Column(db.Integer)
    kitchens = db.Column(db.Integer)
    full_baths = db.Column(db.Integer)
    half_baths = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    fireplaces = db.Column(db.Integer)
    property_style = db.Column(db.String)
    garages = db.Column(db.Integer)
    garage_type = db.Column(db.Integer)
    basement_type = db.Column(db.Integer)
    heat_type = db.Column(db.String)
    gas = db.Column(db.Boolean)
    patio_type = db.Column(db.Integer)
    porch_type = db.Column(db.Integer)
    sewer_type = db.Column(db.Integer)
    water_type = db.Column(db.Integer)
    pool = db.Column(db.Boolean)
    is_residential = db.Column(db.Boolean)

    price_per_sqft = db.Column(db.Float, nullable=True)
    lot_size = db.Column(db.Float)
    lot_size_sqft = db.Column(db.Float)
    location = db.Column(db.Integer)

    condition = db.Column(db.String)
    story_height = db.Column(db.Float)
    paving_type = db.Column(db.Integer)
    origin = db.Column(db.String)
    land_type_code = db.Column(db.String)
    land_use = db.Column(db.Integer, index=True)  # defines whether property is obsolescence or not
    land_tag = db.Column(db.Integer)  # Land Tag - BCPA Internal Use - Notates waterfront, dry lot, etc…;
    water_category = db.Column(db.Integer)  # 6 category groups for land tags.

    address_line_2 = db.Column(db.String)
    address_line_1 = db.Column(db.String)
    address_unit = db.Column(db.String)

    condo_view_location = db.Column(db.String)
    condo_view_influence = db.Column(db.String)
    condo_view_floor = db.Column(db.String)

    assessment_stage = db.Column(db.Integer)
    year = db.Column(db.Integer(), default=2019)
    new_record = db.Column(db.Boolean(), default=False)

    other_adjustment = db.Column(db.Integer)
    other_adjustment_description = db.Column(db.String)

    @hybrid_property
    def condo_code(self):
        """Hybrid property as combination of condo_view_location and condo_view_influence"""
        if self.county == County.MIAMIDADE and self.condo_view_location and self.condo_view_influence:
            return f'{self.condo_view_location}{self.condo_view_influence}'
        return None

    @hybrid_property
    def condo_code_description(self):
        """
        Condo code description
        """
        if self.condo_code:
            if self.county == County.MIAMIDADE:
                return MIAMIDADE_CONDO_CODES.get(self.condo_code)
        return None

    @hybrid_property
    def property_class_description(self):
        """
        Property class code description
        """
        if self.county not in [County.BROWARD, County.MIAMIDADE]:
            return None

        county_codes = PROPERTY_CLASS_DESCRIPTION_MAP.get(self.county)
        if county_codes and self.property_class:
            return county_codes.get(self.property_class)

        return None

    # @hybrid_property
    # def land_tag_description(self):
    #     # We need to display the Land Tag for broward non-condo (houses) CMA
    #     if not self.is_condo and self.county == County.BROWARD and self.land_tag:
    #         return PROPERTY_LAND_TAGS.get(self.county).get(self.land_tag)
    #
    #     return None


class Obsolescence(db.Model):
    __tablename__ = 'obsolescences'
    affected_property_id = db.Column(db.Integer, db.ForeignKey('property.id'),
                                     primary_key=True)
    obs_id = db.Column(db.Integer, db.ForeignKey('property.id'),
                       primary_key=True)


class RoadObsolescence(db.Model):
    __tablename__ = 'road_obsolescences'
    affected_property_id = db.Column(db.Integer, db.ForeignKey('property.id', ondelete='cascade'),
                                     primary_key=True)
    road_id = db.Column(db.Integer, db.ForeignKey('roads.id', ondelete='cascade'),
                        primary_key=True)


class Road(db.Model):
    __tablename__ = 'roads'
    id = db.Column(db.Integer, primary_key=True)
    osm_id = db.Column(db.String, nullable=False)
    type = db.Column(db.String)
    geometry = db.Column(Geometry(geometry_type='LINESTRING', srid=4326), nullable=False)
    county = db.Column(db.String)

    affected_properties = db.relationship('RoadObsolescence',
                                          foreign_keys=[RoadObsolescence.road_id],
                                          backref=db.backref('road', lazy='joined'),
                                          lazy='dynamic',
                                          cascade='all, delete-orphan')


class Property(AbstractProperty):
    __tablename__ = 'property'

    # Relationships
    # sales = relationship("Sale", order_by="desc(Sale.date)", lazy='joined')
    sales = relationship("Sale", lazy='joined')
    assessments = relationship("Assessment", lazy='joined')
    gis = relationship('PropertyGis', lazy='joined')
    # last_assessment = relationship(
    #     "Assessment",
    #     order_by="desc(AssessmentDate.valuation_date)",
    #     primaryjoin="and_(Property.id==foreign(Assessment.property_id), Assessment.assessment_id==AssessmentDate.id)",
    #     viewonly=True,
    #     uselist=False
    # )
    photos = relationship('PropertyPhoto', lazy='select')

    # owners = relationship("Owner")
    owners = db.relationship(
        "Owner",
        order_by="desc(Owner.created_on)",
        primaryjoin="and_(Property.id==foreign(Owner.property_id), Owner.data_source=='assessment')"
    )

    obsolescences = db.relationship('Obsolescence',
                                    foreign_keys=[Obsolescence.affected_property_id],
                                    backref=db.backref('affected_property', lazy='joined'),
                                    lazy='select',
                                    cascade='all, delete-orphan')

    roads = db.relationship('RoadObsolescence',
                            foreign_keys=[RoadObsolescence.affected_property_id],
                            backref=db.backref('affected_property', lazy='joined'),
                            lazy='select',
                            cascade='all, delete-orphan')

    affected_properties = db.relationship('Obsolescence',
                                          foreign_keys=[Obsolescence.obs_id],
                                          backref=db.backref('obs', lazy='joined'),
                                          lazy='select',
                                          cascade='all, delete-orphan')

    @classmethod
    def is_exists(cls, p):
        obj = cls.query.filter_by(apn=p['apn'], county=p['county'])
        if obj.first():
            return True
        return False

    @classmethod
    def update_if_exists(cls, p):
        obj = cls.query.filter_by(apn=p['apn'], county=p['county'])
        try:
            if obj.first():  # update if exists
                obj.update({**p})
                # else:
                #     new_obj = cls(**p)
                #     db.session.add(new_obj)
                db.session.commit()
                print(f'updated property with apn {p["apn"]}')
        except IntegrityError as e:
            db.session.rollback()
            print(f'failed to update property with apn {p["apn"]} due to {e.orig.args}')
            return e.orig.args
        return None

    @classmethod
    def update(cls, obj, p):
        try:
            obj.update({**p})
            db.session.commit()
            print(f'updated property with apn {p["apn"]}')
        except IntegrityError as e:
            db.session.rollback()
            print(f'failed to update property with apn {p["apn"]} due to {e.orig.args}')
            return e.orig.args
        return None

    @classmethod
    def insert(cls, p):
        try:
            new = cls(**p)
            db.session.add(new)
            db.session.commit()
            print(f'inserted new property with apn {p["apn"]}')
        except IntegrityError as e:
            db.session.rollback()
            return e.orig.args
        return None

    @property
    def recently_build(self):
        if not self.age:
            return False
        return self.age > (date.today().year - 5)

    @property
    def is_disqualified(self):
        return not self.last_any_sale.arms_length

    @property
    def last_any_sale(self):
        if self.sales:
            self.sales.sort(key=lambda c: (c.arms_length, c.date), reverse=True)
            return self.sales[0]
        return None

    @property
    def last_sale(self):
        if self.sales:
            self.sales.sort(key=lambda c: (c.arms_length, c.date), reverse=True)
            for sale in self.sales:
                if sale.arms_length:
                    return sale
        return None

    @property
    def buyer_full_name(self):
        if not self.last_sale:
            return None
        return f'{self.last_sale.buyer_first_name or ""} {self.last_sale.buyer_last_name or ""}'.strip()

    @property
    def seller_full_name(self):
        if not self.last_sale:
            return None
        return f'{self.last_sale.seller_first_name or ""} {self.last_sale.seller_last_name or ""}'.strip()


class PropertyOriginal(AbstractProperty):
    """
    Model to store original property data
    """
    __tablename__ = 'property_original'


class PropertyGis(db.Model, UpsertMixin):
    __tablename__ = 'property_gis'

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer,
                            db.ForeignKey("property.id"), nullable=False, onupdate='CASCADE',
                            index=True)
    apn = db.Column(db.String)
    county = db.Column(db.String)
    geometry = db.Column(Geometry())


# TODO: how to relate to the id? there might be error during property db.commit
class PropertyValidation(db.Model, ValidationMixin):
    id = db.Column(db.Integer, primary_key=True)
    apn = db.Column(db.String())
    county = db.Column(db.String())
    errors = db.Column(db.JSON)


class SuffPropertySchema(Schema):
    county = fields.String(data_key='county', missing='suffolk')
    apn = fields.String(data_key='apn', required=True)
    street = fields.String(data_key='street', missing=None, allow_none=True)
    number = fields.String(data_key='number', missing=None, allow_none=True)
    town = fields.String(data_key='town', missing=None)
    zip = fields.Integer(data_key='zip', missing=None)
    coordinate_x = fields.Float(data_key='coordinate_x', missing=None)
    coordinate_y = fields.Float(data_key='coordinate_y', missing=None)
    undefined_field = fields.String(data_key='undefined_field', missing=None)
    property_style = fields.String(data_key='property_style', missing=None, allow_none=True)
    gla_sqft = fields.Float(data_key='gla_sqft', missing=None)
    story_height = fields.Float(data_key='story_height', missing=None)
    age = fields.Integer(data_key='age', missing=None, allow_none=True)
    basement_type = fields.String(data_key='basement_type', missing=None)
    full_baths = fields.Integer(data_key='full_baths', missing=None)
    half_baths = fields.Integer(data_key='half_baths', missing=None)
    bedrooms = fields.Integer(data_key='bedrooms', missing=None)
    fireplaces = fields.Integer(data_key='fireplaces', missing=None)
    rooms = fields.Integer(data_key='rooms', missing=None)
    kitchens = fields.Integer(data_key='kitchens', missing=None)
    heat_type = fields.String(data_key='heat_type', missing=None)
    condition = fields.String(data_key='condition', missing=None)
    effective_age = fields.Integer(data_key='effective_age', missing=None)
    print_key = fields.String(data_key='print_key', missing=None)
    state = fields.String(data_key='state', missing=None)
    address_line_2 = fields.String(data_key='address_line_2', missing=None)
    address_line_1 = fields.String(data_key='address_line_1', missing=None)
    address = fields.String(data_key='address', missing=None)
    section = fields.String(data_key='section', missing=None)
    block = fields.String(data_key='block', missing=None)
    lot = fields.String(data_key='lot', missing=None)
    is_residential = fields.Boolean(data_key='is_residential', missing=None)


class PropertySchema(Schema):
    """
    Property schema used to validate Data Tree.
    """

    apn = fields.String(data_key='apn', required=True)
    county = fields.String(data_key='county', missing='broward')
    school_district = fields.Integer(data_key='school_district', missing=None)
    section = fields.String(data_key='section', missing=None)
    block = fields.String(data_key='block', missing=None)
    is_residential = fields.Boolean(data_key='is_residential', missing=None)

    undefined_field = fields.String(data_key='undefined_field', missing=None)
    lot = fields.String(data_key='lot', missing=None)

    address = fields.String(data_key='address', missing=None)
    street = fields.String(data_key='street', missing=None, allow_none=True)
    number = fields.String(data_key='number', missing=None, allow_none=True)

    town = fields.String(data_key='town', missing=None)
    city = fields.String(data_key='city', missing=None)
    state = fields.String(data_key='state', missing=None)
    zip = fields.Integer(data_key='zip', missing=None)
    latitude = fields.Float(data_key='latitude', missing=None)
    longitude = fields.Float(data_key='longitude', missing=None)
    is_condo = fields.Boolean(data_key='is_condo', missing=None)
    is_listed = fields.Boolean(data_key='is_listed', missing=None)

    hamlet = fields.String(data_key='hamlet', missing=None)
    property_class = fields.Integer(data_key='property_class', missing=None, allow_none=True)
    property_class_type = fields.Integer(data_key='property_class_type', missing=None, allow_none=True)

    age = fields.Integer(data_key='age', missing=None, allow_none=True)
    gla_sqft = fields.Float(data_key='gla_sqft', missing=None)
    under_air_gla_sqft = fields.Float(data_key='under_air_gla_sqft', missing=None)
    waterfront = fields.Boolean(data_key='waterfront', missing=None)

    rooms = fields.Integer(data_key='rooms', missing=None)
    kitchens = fields.Integer(data_key='kitchens', missing=None)
    full_baths = fields.Integer(data_key='full_baths', missing=None)
    half_baths = fields.Integer(data_key='half_baths', missing=None)
    bedrooms = fields.Integer(data_key='bedrooms', missing=None)
    fireplaces = fields.Integer(data_key='fireplaces', missing=None)
    property_style = fields.String(data_key='property_style', missing=None, allow_none=True)

    garages = fields.Integer(data_key='garages', missing=None)
    garage_type = fields.Integer(data_key='garage_type', missing=None)
    basement_type = fields.String(data_key='basement_type', missing=None)

    heat_type = fields.String(data_key='heat_type', missing=None)
    gas = fields.Boolean(data_key='gas', missing=None)
    patio_type = fields.Integer(data_key='patio_type', missing=None)
    porch_type = fields.Integer(data_key='porch_type', missing=None)
    sewer_type = fields.Integer(data_key='sewer_type', missing=None)
    water_type = fields.Integer(data_key='water_type', missing=None)
    pool = fields.Boolean(data_key='pool', missing=None)

    price_per_sqft = fields.Float(data_key='price_per_sqft', missing=None)
    lot_size = fields.Float(data_key='lot_size', missing=None, allow_none=True)
    location = fields.Integer(data_key='location', missing=None)

    district = fields.String(data_key='district', missing=None)
    print_key = fields.String(data_key='print_key', missing=None)
    village = fields.String(data_key='village', missing=None)
    legal = fields.String(data_key='legal', missing=None)
    subdivision = fields.String(data_key='subdivision', missing=None)

    coordinate_x = fields.Float(data_key='coordinate_x', missing=None)
    coordinate_y = fields.Float(data_key='coordinate_y', missing=None)
    building_code = fields.Integer(data_key='building_code', missing=None)
    data_composite = fields.List(cls_or_instance=fields.Integer(), data_key='data_composite',
                                 allow_none=True, missing=None)
    effective_age = fields.Integer(data_key='effective_age', missing=None)
    lot_size_sqft = fields.Float(data_key='lot_size_sqft', missing=None)
    condition = fields.String(data_key='condition', missing=None)
    story_height = fields.Float(data_key='story_height', missing=None)
    paving_type = fields.Integer(data_key='paving_type', missing=None)
    origin = fields.String(data_key='origin', missing=None)
    land_type_code = fields.String(data_key='land_type_code', missing=None)

    land_use = fields.Integer(data_key='land_use', missing=None)
    land_tag = fields.Integer(data_key='land_tag', missing=None)
    water_category = fields.Integer(data_key='water_category', missing=None)

    address_line_2 = fields.String(data_key='address_line_2', missing=None)
    address_line_1 = fields.String(data_key='address_line_1', missing=None)
    address_unit = fields.String(data_key='address_unit', missing=None)

    condo_view_location = fields.String(data_key='condo_view_location', missing=None)
    condo_view_influence = fields.String(data_key='condo_view_influence', missing=None)

    assessment_stage = fields.Integer(data_key='assessment_stage', missing=None)
    year = fields.Integer(data_key='year', missing=None)
    new_record = fields.Boolean(data_key='new_record', missing=None)

    other_adjustment = fields.Integer(data_key='other_adjustment', missing=None)
    other_adjustment_description = fields.String(data_key='other_adjustment_description', missing=None)


class BrowardPropertySchema(PropertySchema):
    county = fields.String(data_key='county', missing='broward')


class PropertyGISSchema(Schema):
    apn = fields.String(data_key='apn', allow_none=True)
    county = fields.String(data_key='county')

    latitude = fields.Float(data_key='latitude', missing=None)
    longitude = fields.Float(data_key='longitude', missing=None)

    coordinate_x = fields.Float(data_key='coordinate_x', missing=None)
    coordinate_y = fields.Float(data_key='coordinate_y', missing=None)


class PalmbeachPropertySchema(Schema):
    # property id fields
    apn = fields.String(required=True, data_key='apn')
    county = fields.String(data_key='county')
    is_residential = fields.Boolean(data_key='is_residential', missing=None)

    school_district = fields.Integer(missing=None)
    section = fields.String(data_key='section', missing=None)
    block = fields.String(data_key='block', missing=None)
    undefined_field = fields.String(missing=None)
    lot = fields.String(data_key='lot', missing=None)

    town = fields.String(data_key='town', missing=None)
    city = fields.String(data_key='city', missing=None)
    state = fields.String(data_key='state')
    location = fields.Integer(missing=None)

    latitude = fields.Float(missing=None)
    longitude = fields.Float(missing=None)

    is_listed = fields.Boolean(missing=None)
    hamlet = fields.String(missing=None)

    property_style = fields.String(missing=None)
    price_per_sqft = fields.Float(missing=None)
    waterfront = fields.Boolean(missing=None)

    rooms = fields.Integer(missing=None)
    kitchens = fields.Integer(missing=None)

    sewer_type = fields.Integer(missing=None)
    water_type = fields.Integer(missing=None)


class PalmBeachParcelSchema(PalmbeachPropertySchema):
    address = fields.String(data_key='address', missing=None)
    street = fields.String(data_key='street', allow_none=True, missing=None)
    number = fields.String(data_key='number', allow_none=True, missing=None)
    zip = fields.Integer(data_key='zip', missing=None, allow_none=True)
    property_class = fields.Integer(data_key='property_class', missing=None)

    data_composite = fields.List(
        cls_or_instance=fields.Integer(),
        data_key='data_composite',
        allow_none=True,
        missing=None
    )


class PalmbeachCondoSchema(PalmbeachPropertySchema):
    age = fields.Integer(data_key='age', allow_none=True)
    is_condo = fields.Boolean(missing=None)
    building_code = fields.Integer(data_key='building_code', missing=None)
    full_baths = fields.Integer(data_key='full_baths', missing=None)
    half_baths = fields.Integer(data_key='half_baths', missing=None)
    bedrooms = fields.Integer(data_key='bedrooms', missing=None)
    gla_sqft = fields.Float(data_key='gla_sqft', allow_none=True, missing=None)


class PalmbeachResbldSchema(PalmbeachPropertySchema):
    age = fields.Integer(data_key='age', allow_none=True)
    is_condo = fields.Boolean(missing=None)
    building_code = fields.Integer(data_key='building_code', missing=None)
    full_baths = fields.Integer(data_key='full_baths', missing=None)
    half_baths = fields.Integer(data_key='half_baths', missing=None)
    bedrooms = fields.Integer(data_key='bedrooms', missing=None)
    story_height = fields.Float(data_key='story_height', allow_none=True, missing=None)
    lot_size = fields.Float(data_key='lot_size', allow_none=True, missing=None)
    gla_sqft = fields.Float(data_key='gla_sqft', allow_none=True, missing=None)
    gas = fields.Boolean(data_key='gas', missing=None)
    condition = fields.String(data_key='condition', missing=None)
    heat_type = fields.String(data_key='heat_type', allow_none=True, missing=None)


class PalmbeachCombldSchema(PalmbeachPropertySchema):
    age = fields.Integer(data_key='age', allow_none=True)
    gla_sqft = fields.Float(data_key='gla_sqft', allow_none=True, missing=None)
    condition = fields.String(data_key='condition', missing=None)


class PalmbeachLandSchema(PalmbeachPropertySchema):
    lot_size = fields.Float(data_key='lot_size', allow_none=True, missing=None)
    gla_sqft = fields.Float(data_key='gla_sqft', allow_none=True, missing=None)


class PalmbeachObySchema(PalmbeachPropertySchema):
    # gla_sqft = fields.Float(data_key='gla_sqft', allow_none=True, missing=None)
    fireplaces = fields.Integer(data_key='fireplaces', allow_none=True, missing=None)
    garages = fields.Integer(data_key='garages', allow_none=True, missing=None)
    pool = fields.Boolean(data_key='pool', missing=None)

    garage_type = fields.Integer(data_key='garage_type', allow_none=True, missing=None)
    basement_type = fields.Integer(data_key='basement_type', allow_none=True, missing=None)
    patio_type = fields.Integer(data_key='patio_type', allow_none=True, missing=None)
    porch_type = fields.Integer(data_key='porch_type', allow_none=True, missing=None)

    @staticmethod
    def adjust_value_type(value):
        if value is None or value == '':
            return None
        return value

    @pre_load
    def adjust_oby_fields(self, data, **kwargs):
        data['basement_type'] = self.adjust_value_type(data.get('basement_type'))
        data['garage_type'] = self.adjust_value_type(data.get('garage_type'))
        data['garage_type'] = self.adjust_value_type(data.get('garage_type'))
        data['patio_type'] = self.adjust_value_type(data.get('patio_type'))
        data['porch_type'] = self.adjust_value_type(data.get('porch_type'))

        return data


class NassauPropertySchema(Schema):
    """
    Schema will be used to validate RESIDENTIAL property
    data.
    """
    apn = fields.String(required=True, data_key='PARID')
    is_residential = fields.Boolean(data_key='is_residential', missing=None)

    county = fields.String(missing='nassau')
    school_district = fields.Integer(required=True, data_key='SCH')
    section = fields.String()
    block = fields.String()
    undefined_field = fields.String()  # Unit
    lot = fields.String()
    building_code = fields.Integer()

    address = fields.String()
    street = fields.String(data_key='ADRSTR', allow_none=True)
    number = fields.String()
    town = fields.String(data_key='T')
    # TODO: zip and state missing at residential.asc but present in sale data
    state = fields.String(missing='NY')
    zip = fields.String(missing=None)

    coordinate_x = fields.Float(data_key='X_COORD', allow_none=True)
    coordinate_y = fields.Float(data_key='Y_COORD', allow_none=True)

    # TODO: discuss...flag also present among sale data
    is_condo = fields.Boolean()
    is_listed = fields.Boolean(missing=None)

    # TODO: missing at input
    hamlet = fields.String(missing=None)

    property_class = fields.Integer(required=True, data_key='LUC')

    age = fields.Integer(data_key='YRBLT', allow_none=True)

    gla_sqft = fields.Float(data_key='SFLA', allow_none=True)

    waterfront = fields.Boolean()

    # TODO: nassau missing number of kitchens
    rooms = fields.Integer(data_key='RMT')
    kitchens = fields.Integer(missing=None)
    full_baths = fields.Integer(data_key='FIX')
    half_baths = fields.Integer(data_key='FIX_1')
    # TODO: nassau missing number of bedrooms
    bedrooms = fields.Integer(missing=None)
    fireplaces = fields.Integer(data_key='WBF')
    property_style = fields.String(data_key='ST', allow_none=True)

    garages = fields.Integer(data_key='BS', allow_none=True)
    garage_type = fields.Integer(missing=None)
    basement_type = fields.Integer(data_key='B', allow_none=True)
    heat_type = fields.String(data_key='H')
    # TODO: discuss...fields are missing in Nassau data
    gas = fields.Boolean(missing=None)
    patio_type = fields.Integer(missing=None)
    porch_type = fields.Integer(missing=None)
    sewer_type = fields.Integer(missing=None)
    water_type = fields.Integer(missing=None)
    pool = fields.Boolean(missing=None)

    price_per_sqft = fields.Float(missing=None, precision=3)

    # TODO: there is total_sale acres in sales data. Maybe we need that input instead?
    lot_size = fields.Float(data_key='ACRES')

    location = fields.Integer(data_key='LO', allow_none=True)

    @pre_load
    def parse_apn(self, data, **kwargs):
        apn = data['PARID']
        section = apn[:2].lstrip('0')
        block = apn[2:7]

        if block[-1] != ' ':
            block = '-'.join([block[:3].lstrip('0'), block[3:].lstrip('0')]).lstrip(
                '0').strip(' ')
        else:
            block = block.strip(' ').lstrip('0')
        if len(apn) == 12:
            lot = apn[7:12]
            if lot[-1] == '0':
                lot = lot[:-1].lstrip('0')
            elif lot[-1].isdigit():
                lot = '-'.join([lot[:-1].lstrip('0'), lot[-1]])
            else:
                lot = lot.lstrip('0')
            unit = None
            building_code = None
            data['is_condo'] = False
        else:
            # is_condo
            lot = apn[7:11].lstrip('0')
            building_code = apn[14:18].lstrip('0')
            unit = apn[18:].lstrip('0')
            data['is_condo'] = True

        data['section'] = section
        data['block'] = block
        data['lot'] = lot
        data['undefined_field'] = unit
        data['building_code'] = building_code
        return data

    @pre_load
    def adjust_address(self, data, **kwargs):
        data['address'] = ' '.join([data.get('ADRNO', ''),
                                    data.get('ADRADD', ''),
                                    data.get('ADRSTR', ''),
                                    data.get('ADRSUF', '')])

        data['number'] = ' '.join([data.get('ADRNO', ''),
                                   data.get('ADRADD', '')]).strip()

        data['waterfront'] = True if data.get('COD') in [
            '2B', '2C', '2L', '2O', '2S', '2W'] else False

        return data

    @pre_load
    def adjust_garages(self, data, **kwargs):
        data['garages'] = data.get('BS', 1)
        return data


class SuffolkPropertySchema(Schema):
    """
    Schema will be used to validate Suffolk property
    data.
    """
    apn = fields.String(data_key='APN', missing=None)
    is_residential = fields.Boolean(data_key='is_residential', missing=None)

    county = fields.String(missing='suffolk')
    # will be comming from assessment data
    school_district = fields.Integer(missing=None)
    section = fields.Float(data_key='section', missing=None)
    block = fields.Float(data_key='block', missing=None)
    lot = fields.Float(data_key='lot', missing=None)
    street = fields.String(data_key='loc_st_name', missing=None)
    number = fields.String(data_key='loc_st_nbr', missing=None)
    address = fields.String(missing=None)
    address_line_1 = fields.String(missing=None)
    address_line_2 = fields.String(missing=None)
    zip = fields.Integer(data_key='loc_zip', missing=None)
    coordinate_x = fields.Float(data_key='grid_east', missing=None)
    coordinate_y = fields.Float(data_key='grid_north', missing=None)
    town = fields.String(data_key='loc_muni_name', missing=None)
    state = fields.String(missing=None)
    heat_type = fields.String(data_key='heat_type', missing=None)
    undefined_field = fields.String(data_key='muni_code', missing=None)
    print_key = fields.String(data_key='print_key', missing=None)

    # TODO: fields missing at source
    is_condo = fields.Boolean(missing=None)
    is_listed = fields.Boolean(missing=None)
    hamlet = fields.String(missing=None)
    # will be comming from assessment data
    property_class = fields.Integer(missing=None)
    garage_type = fields.Integer(missing=None)
    gas = fields.Boolean(missing=None)
    patio_type = fields.Integer(missing=None)
    porch_type = fields.Integer(missing=None)
    sewer_type = fields.Integer(missing=None)
    water_type = fields.Integer(missing=None)
    location = fields.Integer(data_key='LO', allow_none=True, missing=None)
    price_per_sqft = fields.Float(missing=None)

    age = fields.Integer(data_key='AGE', missing=None)
    gla_sqft = fields.Float(data_key='GLA', missing=None)
    waterfront = fields.Boolean()
    rooms = fields.Integer(data_key='ROOMS', missing=None)
    kitchens = fields.Integer(data_key='KITCHENS', missing=None)
    full_baths = fields.Integer(missing=None)
    half_baths = fields.Integer(missing=None)
    bedrooms = fields.Integer(data_key='BEDROOMS', missing=None)
    fireplaces = fields.Integer(data_key='FIREPLACES', missing=None)
    property_style = fields.String(data_key='STYLE', missing=None)
    garages = fields.Integer(data_key='GARAGE', missing=None)
    basement_type = fields.Integer(allow_none=True, missing=None)
    pool = fields.Boolean(missing=None)
    lot_size = fields.Float(data_key='LOT_SIZE', missing=None)

    @pre_load
    def dsbl(self, data, **kwargs):
        # dsbl = data['DSBL'].strip().split('-')
        # data['town'] = str(round(int(dsbl[0]), -2)) if dsbl[0] else None
        # data['town'] = data.get('loc_muni_name', '')
        # data['section'] = dsbl[1] if len(dsbl) > 1 else None
        # data['block'] = dsbl[2] if len(dsbl) > 2 else None
        # data['lot'] = dsbl[3] if len(dsbl) > 3 else None

        if data['WATERFRONT'] == 'Y':
            data['waterfront'] = True
        elif data['WATERFRONT'] == 'N':
            data['waterfront'] = False
        else:
            data['waterfront'] = None

        data['pool'] = None
        if data['POOL'] == 'Y':
            data['pool'] = True
        elif data['POOL'] == 'N':
            data['pool'] = False

        data['full_baths'] = None
        data['half_baths'] = None
        if data['BATHS']:
            split = str(data['BATHS']).strip().split('.')
            data['full_baths'] = int(split[0].strip()) \
                if split and split[0] else 0
            data['half_baths'] = 1 if len(split) > 1 and int(split[1].strip()) == 5 else 0

        loc_zip = str(data.get('loc_zip', ''))[:5]
        address_line_1 = ' '.join([data.get('loc_st_nbr', ''), data.get('loc_st_name', ''),
                                   data.get('loc_mail_st_suff', '')]).strip()
        address_line_2 = ' '.join([data.get('loc_unit_name', ''), data.get('loc_unit_nbr', '')]).strip()

        address_line_3 = ''
        if data.get('loc_muni_name', '').strip() and loc_zip.strip():
            address_line_3 = ' '.join([data.get('loc_muni_name', ''), 'NY', loc_zip]).strip()

        if address_line_1 and address_line_2 and address_line_3:
            data['address'] = ', '.join([address_line_1, address_line_2, address_line_3])
        elif address_line_1 and address_line_2:
            data['address'] = ', '.join([address_line_1, address_line_2])
        elif address_line_1 and address_line_3:
            data['address'] = ', '.join([address_line_1, address_line_3])
        else:
            data['address'] = address_line_1

        data['address'] = data['address'].strip(',')
        data['address_line_1'] = address_line_1
        data['address_line_2'] = address_line_2
        data['state'] = 'NY'
        # adjusting basement
        bsmt = data['BASEMENT'] or ''
        data['basement_type'] = next((key for key, name in BASEMENT_TYPE_MAP['suffolk'].items()
                                      if name == bsmt.lower()), None)

        return data


class GeneralSchema(Schema):
    """
    General Schema according to GlobalCMA.drawio
    We use general schema to map all the row fields. Later
    we distribute this row fields to the corresponding tables.
    """
    # Property indentification information
    fips_code = fields.String(data_key='FIPS')  # County.fips_code
    property_id = fields.Integer(data_key='PropertyID')
    apn = fields.String(data_key='APN')  # Property.APN
    tax_account_number = fields.String(data_key='TaxAccountNumber',
                                       allow_none=True)

    # property address information
    full_street_address = fields.String(data_key='SitusFullStreetAddress')
    house_number = fields.String(data_key='SitusHouseNbr',
                                 allow_none=True)
    street = fields.String(data_key='SitusStreet')
    mode = fields.String(data_key='SitusMode',
                         allow_none=True)
    unit_number = fields.String(data_key='SitusUnitNbr',
                                allow_none=True)
    unit_type = fields.String(data_key='SitusUnitType',
                              allow_none=True)
    city = fields.String(data_key='SitusCity')
    state = fields.String(data_key='SitusState')
    zip5 = fields.String(data_key='SitusZIP5')
    zip4 = fields.String(data_key='SitusZIP4',
                         allow_none=True)
    carrier_code = fields.String(data_key='SitusCarrierCode',
                                 allow_none=True)
    latitude = fields.Float(data_key='SitusLatitude')
    longitude = fields.Float(data_key='SitusLongitude')
    geo_status_code = fields.String(data_key='SitusGeoStatusCode')

    # property information
    class_id = fields.String(data_key='PropertyClassID',
                             allow_none=True)
    land_use_code = fields.String(data_key='LandUseCode')
    county_land_use_code = fields.String(data_key='CountyLandUseCode',
                                         allow_none=True)
    zoning = fields.String(data_key='Zoning',
                           allow_none=True)
    census_tract = fields.String(data_key='SitusCensusTract')
    census_block = fields.String(data_key='SitusCensusBlock')
    mobile_home_ind = fields.String(data_key='MobileHomeInd')
    timeshare_code = fields.String(data_key='TimeshareCode')
    school_district_name = fields.String(
        data_key='SchoolDistrictName')

    # lot information
    frontage_feet = fields.Integer(data_key='LotSizeFrontageFeet',
                                   allow_none=True)
    depth_feet = fields.Integer(data_key='LotSizeDepthFeet')
    acres = fields.String(data_key='LotSizeAcres')
    square_foot = fields.Integer(data_key='LotSizeSqFt')

    # owner information
    owner1_full_name = fields.String(data_key='OwnerNAME1FULL')
    owner1_is_corp = fields.String(data_key='Owner1CorpInd',
                                   allow_none=True)
    owner2_full_name = fields.String(data_key='OwnerNAME2FULL',
                                     allow_none=True)
    owner2_is_corp = fields.String(data_key='Owner2CorpInd',
                                   allow_none=True)
    owner_occupied = fields.String(data_key='OwnerOccupied',
                                   allow_none=True)
    owner1_rights = fields.String(data_key='Owner1OwnershipRights',
                                  allow_none=True)

    # building square footage information
    building_area = fields.String(data_key='BuildingArea')
    building_area_indicator = fields.String(data_key='BuildingAreaInd',
                                            allow_none=True)
    sum_building_sqft = fields.String(data_key='SumBuildingSqFt')
    sum_living_area_sqft = fields.String(data_key='SumLivingAreaSqFt',
                                         allow_none=True)
    sum_ground_floor_sqft = fields.String(data_key='SumGroundFloorSqFt',
                                          allow_none=True)
    sum_gross_area_sqft = fields.String(data_key='SumGrossAreaSqFt',
                                        allow_none=True)
    sum_adj_area_sqft = fields.String(data_key='SumAdjAreaSqFt',
                                      allow_none=True)

    attic_sqft = fields.Integer(data_key='AtticSqFt',
                                allow_none=True)
    attic_sqft_unfinished = fields.Integer(
        data_key='AtticUnfinishedSqFt', allow_none=True)
    attic_sqft_finished = fields.Integer(data_key='AtticFinishedSqFt',
                                         allow_none=True)

    sum_basement_sqft = fields.Integer(data_key='SumBasementSqFt',
                                       allow_none=True)
    basement_unfinished_sqft = fields.Integer(
        data_key='BasementUnfinishedSqFt', allow_none=True)
    basement_finished_sqft = fields.Integer(
        data_key='BasementFinishedSqFt', allow_none=True)

    sum_garage_sqft = fields.Integer(data_key='SumGarageSqFt',
                                     allow_none=True)
    garage_unfinished_sqft = fields.Integer(data_key='GarageUnFinishedSqFt', allow_none=True)
    garage_finished_sqft = fields.Integer(data_key='GarageFinishedSqFt',
                                          allow_none=True)

    year_built = fields.String(data_key='YearBuilt',
                               allow_none=True)
    effective_year_built = fields.String(data_key='EffectiveYearBuilt',
                                         allow_none=True)

    bedrooms = fields.Float(data_key='Bedrooms')
    total_rooms = fields.Float(data_key='TotalRooms')
    # First American calculated number of bath rooms
    total_baths_calculated = fields.Float(data_key='BathTotalCalc')
    full_baths = fields.Float(data_key='BathFull')
    half_baths = fields.Float(data_key='BathsPartialNbr')
    fixture_baths = fields.Float(data_key='BathFixturesNbr',
                                 allow_none=True)
    amenities = fields.String(data_key='Amenities',
                              allow_none=True)

    air_condition_code = fields.Integer(data_key='AirConditioningCode',
                                        allow_none=True)
    basement_code = fields.Integer(data_key='BasementCode',
                                   allow_none=True)
    building_class_code = fields.Integer(data_key='BuildingClassCode',
                                         allow_none=True)
    building_condition_code = fields.Integer(
        data_key='BuildingConditionCode', allow_none=True)
    construction_type_code = fields.Integer(
        data_key='ConstructionTypeCode', allow_none=True)
    # indicates there is a deck
    deck_indicator = fields.Integer(
        data_key='DeckInd', allow_none=True)
    exterior_walls_code = fields.Integer(
        data_key='ExteriorWallsCode', allow_none=True)
    interior_walls_code = fields.Integer(data_key='InteriorWallsCode',
                                         allow_none=True)
    fireplace_code = fields.Integer(data_key='FireplaceCode',
                                    allow_none=True)
    floor_cover_code = fields.Integer(data_key='FloorCoverCode',
                                      allow_none=True)
    garage_type = fields.Integer(data_key='Garage',
                                 allow_none=True)
    heat_code = fields.Integer(data_key='HeatCode',
                               allow_none=True)
    heating_fuel_code = fields.Integer(data_key='HeatingFuelTypeCode',
                                       allow_none=True)
    site_influence_code = fields.String(data_key='SiteInfluenceCode',
                                        allow_none=True)
    garage_parking_number = fields.Integer(data_key='GarageParkingNbr')
    driveway_code = fields.String(data_key='DrivewayCode',
                                  allow_none=True)
    other_rooms = fields.String(data_key='OtherRooms',
                                allow_none=True)
    patio_code = fields.Integer(data_key='PatioCode',
                                allow_none=True)
    pool_code = fields.Integer(data_key='PoolCode',
                               allow_none=True)
    porch_code = fields.Integer(data_key='PorchCode',
                                allow_none=True)
    building_quality_code = fields.Integer(data_key='BuildingQualityCode', allow_none=True)
    roof_cover_code = fields.Integer(data_key='RoofCoverCode',
                                     allow_none=True)
    roof_type_code = fields.Integer(data_key='RoofTypeCode',
                                    allow_none=True)
    sewer_code = fields.Integer(data_key='SewerCode',
                                allow_none=True)
    stories_code = fields.Integer(data_key='StoriesNbrCode',
                                  allow_none=True)
    style_code = fields.Integer(data_key='StyleCode',
                                allow_none=True)
    # "SumResidentialUnits": "0",
    # "SumBuildingsNbr": "0",
    # "SumCommercialUnits": None,

    topography_code = fields.String(data_key='TopographyCode',
                                    allow_none=True)
    water_code = fields.Integer(data_key='WaterCode',
                                allow_none=True)

    # legal description
    lot_code = fields.String(data_key='LotCode',
                             allow_none=True)
    lot_number = fields.String(data_key='LotNbr')
    land_lot = fields.String(data_key='LandLot',
                             allow_none=True)
    block = fields.String(data_key='Block')
    section = fields.String(data_key='Section')
    district = fields.String(data_key='District')
    legal_unit = fields.String(data_key='LegalUnit',
                               allow_none=True)
    municipality = fields.String(data_key='Municipality')

    # "SubdivisionName": None,
    # "SubdivisionPhaseNbr": None,
    # "SubdivisionTractNbr": None,
    # "Meridian": None,
    # "AssessorsMapRef": None,
    # "LegalDescription": None,

    # sale information
    sale_transaction_id = fields.Integer(
        data_key='CurrentSaleTransactionId', allow_none=True)
    sale_document_number = fields.String(
        data_key='CurrentSaleDocNbr', allow_none=True)
    sale_book = fields.String(data_key='CurrentSaleBook',
                              allow_none=True)
    sale_page = fields.String(data_key='CurrentSalePage',
                              allow_none=True)
    sale_recording_date = fields.String(
        data_key='CurrentSaleRecordingDate', allow_none=True)
    sale_contract_date = fields.String(data_key='CurrentSaleContractDate', allow_none=True)
    sale_document_type = fields.String(data_key='CurrentSaleDocumentType', allow_none=True)
    sale_price = fields.Integer(data_key='CurrentSalesPrice',
                                allow_none=True)
    sale_price_code = fields.String(data_key='CurrentSalesPriceCode',
                                    allow_none=True)
    sale_buyer_name_1 = fields.String(data_key='CurrentSaleBuyer1FullName', allow_none=True)
    sale_buyer_name_2 = fields.String(data_key='CurrentSaleBuyer2FullName', allow_none=True)
    sale_seller_name_1 = fields.String(data_key='CurrentSaleSeller1FullName', allow_none=True)
    sale_seller_name_2 = fields.String(data_key='CurrentSaleSeller2FullName', allow_none=True)

    # listing information
    is_listed_flag = fields.String(data_key='IsListedFlag',
                                   allow_none=True)
    is_listed_flag_date = fields.String(data_key='IsListedFlagDate',
                                        allow_none=True)
    is_listed_price_range = fields.String(data_key='IsListedPriceRange',
                                          allow_none=True)

    # vacancy information
    vacant_flag = fields.String(data_key='VacantFlag',
                                allow_none=True)
    vacant_flag_date = fields.String(data_key='VacantFlagDate',
                                     allow_none=True)


class MiamidadePropertySchema(Schema):
    apn = fields.String(required=True, data_key='apn')
    is_residential = fields.Boolean(data_key='is_residential', missing=None)

    county = fields.String(data_key='county', missing='miamidade')
    school_district = fields.Integer(missing=None)
    section = fields.String(data_key='section', missing=None)
    block = fields.String(data_key='block', missing=None)
    undefined_field = fields.String(missing=None)
    lot = fields.String(data_key='lot', missing=None)

    address = fields.String(data_key='address', missing=None)
    street = fields.String(data_key='street', missing=None, allow_none=True)
    number = fields.String(data_key='number', missing=None, allow_none=True)
    town = fields.String(data_key='town', missing=None)
    city = fields.String(data_key='city', missing=None)

    # TODO: state is missing in data, but present in sale data as 'STATE_PARCEL_ID'
    state = fields.String(missing="FL")
    zip = fields.Integer(data_key='zip', missing=None)

    latitude = fields.Float(missing=None)
    longitude = fields.Float(missing=None)

    coordinate_x = fields.Float(missing=None)
    coordinate_y = fields.Float(missing=None)

    is_condo = fields.Boolean(data_key='is_condo', missing=None)
    is_listed = fields.Boolean(missing=None)

    hamlet = fields.String(missing=None)
    # TODO: is it get from zoning or land_use?
    property_class = fields.Integer(data_key='property_class', allow_none=True, missing=None)
    building_code = fields.Integer(missing=None)
    data_composite = fields.List(cls_or_instance=fields.Integer(), missing=None)

    age = fields.Integer(data_key='age', missing=None, allow_none=True)
    gla_sqft = fields.Float(data_key='gla_sqft', missing=None)
    waterfront = fields.Boolean(data_key='waterfront', missing=None)

    rooms = fields.Integer(missing=None)
    kitchens = fields.Integer(missing=None)
    full_baths = fields.Integer(data_key='full_baths', missing=None)

    # TODO: missing half_baths in data source, but present in GIS data file.
    half_baths = fields.Integer(missing=None)
    bedrooms = fields.Integer(data_key='bedrooms', missing=None)
    fireplaces = fields.Integer(missing=None)
    property_style = fields.String(missing=None)
    garages = fields.Integer(missing=None)
    garage_type = fields.Integer(missing=None)
    basement_type = fields.String(missing=None)
    heat_type = fields.String(missing=None)
    gas = fields.Boolean(missing=None)

    patio_type = fields.Integer(data_key='patio_type', missing=None)
    porch_type = fields.Integer(missing=None)
    sewer_type = fields.Integer(missing=None)
    water_type = fields.Integer(data_key='is_waterfront', missing=None)

    pool = fields.Boolean(data_key='is_pool', missing=None)
    condition = fields.String(data_key='condition_type', missing=None)
    story_height = fields.Float(missing=None)
    paving_type = fields.Integer(data_key='paving_type', missing=None)

    price_per_sqft = fields.Float(missing=None)
    lot_size = fields.Float(data_key='lot_size', allow_none=True)
    location = fields.Integer(missing=None)


class PropertyPhotoSchema(BaseSchema):
    class Meta:
        from app.database.models.property_photo import PropertyPhoto
        model = PropertyPhoto

    url = fields.String(dump_only=True)
    rank = fields.Integer(dump_only=True)


class PropertyCountySchema(BaseSchema):
    class Meta:
        model = PropertyCounty


class BasePropertyModelSchema(BaseSchema):
    class Meta:
        model = Property
        exclude = ('assessments', 'sales', 'geo')

    owners = Nested('OwnerModelSchema', many=True, dump_only=True)
    photos = Nested(PropertyPhotoSchema, many=True)
    property_county = Nested(PropertyCountySchema(), many=False, dump_only=True)


class PublicPropertySchema(BaseSchema):
    class Meta:
        model = Property
        exclude = ('assessments', 'sales', 'geo')

    full_name = fields.String()

    # Override attribute names
    property_id = fields.Integer(attribute='id', dump_only=True)
    full_address = fields.String(attribute='address', dump_only=True)
    address_zip = fields.Integer(attribute='zip', dump_only=True)
    address_street = fields.String(attribute='street', dump_only=True)
    address_number = fields.String(attribute='number', dump_only=True)
    address_state = fields.String(attribute='state', dump_only=True)
    address_city = fields.String(attribute='city', dump_only=True)
    address_latitude = fields.Float(attribute='latitude', dump_only=True)
    address_longitude = fields.Float(attribute='longitude', dump_only=True)
    address_iscondo = fields.Boolean(attribute='is_condo', dump_only=True)
    address_line1 = fields.String(attribute='address_line_1', dump_only=True)
    address_line2 = fields.String(attribute='address_line_2', dump_only=True)
    owners = fields.List(cls_or_instance=fields.String(), attribute='owner_full_names', dump_only=True)


class PropertyModelSchema(BasePropertyModelSchema):
    last_sale_price = fields.Integer(allow_none=True)
    last_sale_date = fields.Date(allow_none=True)
    buyer_full_name = fields.String(dump_only=True)
    seller_full_name = fields.String(dump_only=True)
    condo_code = fields.String(dump_only=True)
    condo_code_description = fields.String(dump_only=True)
    property_class_description = fields.String(dump_only=True)
    obs_geojson = fields.List(cls_or_instance=fields.Dict(),
                              dump_only=True,
                              allow_none=True)


class PropertyOverriddenSchema(PropertyModelSchema):
    class Meta:
        model = PropertyOriginal
        exclude = ('geo',)


class AdjustmentResultSchema(Schema):
    """
    Declare schema for the Single CMA adjustment results
    """
    key = fields.String()
    adjusted = fields.Boolean()
    value = fields.Integer()
    name = fields.String()
    inventory_rule_id = fields.Integer(allow_none=True)
    rule_value = fields.String()
    subject_rule_value = fields.String()
    subject_value = fields.String()
    comp_value = fields.String()
    comp_percent_value = fields.Integer()
    subject_percent_value = fields.Integer()


@dataclass
class CmaNotification:
    """
    Class represents CMA alerts notification object
    """
    status: str
    message: str


CmaNotificationSchema = marshmallow_dataclass.class_schema(CmaNotification)


class SubjectPropertySchema(PropertyModelSchema):
    print_sale_info = fields.Boolean(dump_only=True)
    market_value = fields.Integer(dump_only=True)
    assessment_value = fields.Integer(dump_only=True)
    cma_notification = Nested(CmaNotificationSchema(), many=False, dump_only=True)


class ObsoResultsSchema(Schema):
    """Schema for obsolescence since florida may have multiple obsolescence"""
    key = fields.String()
    adjusted = fields.Boolean()
    value = fields.Integer()
    name = fields.String()
    rule_value = fields.String()
    subject_value = fields.String()
    comp_value = fields.String()
    subject_obsolescences = fields.Dict()
    comp_obsolescences = fields.Dict()


class ComparativePropertySchema(PropertyModelSchema):
    adjustment_delta_value = fields.Float(dump_only=True)
    adjusted_market_value = fields.Float(dump_only=True)
    adjustments = Nested(AdjustmentResultSchema(), many=True, dump_only=True)
    # obso_result = Nested(ObsoResultsSchema(), dump_only=True)
    proximity = fields.Float()
    priority = fields.Integer()
    status = fields.String()
    comp_assessment_value = fields.Integer(dump_only=True)
    comp_market_value = fields.Integer(dump_only=True)
