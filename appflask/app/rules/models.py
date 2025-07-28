import datetime
from collections import OrderedDict

from marshmallow import Schema, fields
from marshmallow_sqlalchemy.fields import Nested
from pandas.core.common import flatten
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.types import Integer, String, Numeric, ARRAY, Boolean, Float

from app import db
from app.database.models.property import NASSAU_VILLAGE_CODES
from app.rules.adjustments import ALL_ADJUSTMENTS, RULE_INVENTORY, RULE_MISC
from app.rules.obsolescence import ALL_OBSOLESCENCE, RULE_OBSOLESCENCE
from app.rules.selections import ALL_SELECTIONS, RULE_SELECTION
from app.settings.models import BaseSchema
from app.utils.constants import SqftInAcre

ALL_MISC_RULES = OrderedDict([
    ('HIGH_SALE_DATE_LOWER', {
        'name': 'High Sale Date Lower',
        'rule_type': RULE_MISC,
        'rule_field': 'high_sale_date_lower',
    }),
    ('HIGH_SALE_DATE_HIGHER', {
        'name': 'High Sale Date Higher',
        'rule_type': RULE_MISC,
        'rule_field': 'high_sale_date_higher',
    }),
])

RULE_TYPES = [RULE_INVENTORY, RULE_SELECTION, RULE_OBSOLESCENCE, RULE_MISC]

ALL_RULES = ALL_ADJUSTMENTS.copy()
ALL_RULES.update(ALL_SELECTIONS)
ALL_RULES.update(ALL_MISC_RULES)
# Add all from obsolescence too
for county_rule in list(ALL_OBSOLESCENCE.values()):
    ALL_RULES.update(county_rule.items())


class PropertiesRules(db.Model):
    __tablename__ = 'properties_rules'
    id = db.Column(Integer, primary_key=True)

    rule_name = db.Column(String, index=True)

    parent_id = db.Column(Integer, ForeignKey('properties_rules.id'), nullable=True)
    parent = relationship('PropertiesRules', remote_side=[id], join_depth=3, lazy='immediate')

    county = db.Column(String(), nullable=True)
    subject_sales_from = db.Column(db.Date())
    town = db.Column(String(), nullable=True)
    village = db.Column(String())
    year = db.Column(db.Integer, nullable=True)

    cost_of_sale = db.Column(db.Integer)
    water = db.Column(db.Integer)

    # adjustment coefficient: percent % of adjustment to be applied
    condo_view_floor = db.Column(db.Integer)
    age = db.Column(db.Float)

    # Obsolescence rules are simply an array of percentages (Decimals). No need to create a separate table for them
    obsolescence_rules = db.Column(ARRAY(Numeric(precision=6, scale=3)), nullable=True)

    # TODO: These two are not implemented in the functionality yet.
    # REQ: Client chooses which adjustments will be done for this county/area
    # REQ: Client decides which are required for Mass CMA, otherwise it cannot be computed
    adjustments_required = db.Column(ARRAY(String), nullable=True)
    adjustments_all = db.Column(ARRAY(String), nullable=True)

    last_updated = db.Column(db.DateTime(), default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    # Load all rules
    inventory_rules = relationship('InventoryRules', backref='parent',
                                   lazy='joined',
                                   passive_deletes='all')
    selection_rules = relationship('SelectionRules', uselist=False, backref='parent',
                                   lazy='joined',
                                   passive_deletes='all')

    __table_args__ = (
        # Protect from duplicate records
        UniqueConstraint('county', 'town', 'village', 'year', name='uc_properties_rules'),
        # Index('ix_properties_rules_county_year', 'county', 'year', unique=True),
        # Index('ix_properties_rules_county_town_year', 'county', 'town', 'year', unique=True),
    )

    @validates('village')
    def validate_village(self, key, village):
        if village:
            assert self.county == 'nassau'
            assert village in NASSAU_VILLAGE_CODES
        return village

    @staticmethod
    def load_rules(county=None, town=None, village=None, year=None):
        try:
            rules = db.session.query(PropertiesRules).filter(
                PropertiesRules.county == county,
                PropertiesRules.town == town,
                PropertiesRules.year == year,
                PropertiesRules.village == village
            ).one()

            return rules
        except NoResultFound as exc:
            # Seek more generic rules
            if town:
                return PropertiesRules.load_rules(county=county, year=year)
            elif county:
                return PropertiesRules.load_rules()
            else:
                # We have no generic rules at all? Raise exception
                raise exc

    def all_obsolescence_rules_inherit_from_parent(self):
        if self.obsolescence_rules:
            return all(t is None for t in self.obsolescence_rules)
        return True

    def all_inventory_rules_inherit_from_parent(self):
        for ir in self.inventory_rules:
            as_dict = vars(ir)
            as_dict.pop('_sa_instance_state')
            as_dict.pop('id')
            as_dict.pop('parent_id')
            # return all(v is None for v in as_dict.values())
            if any(list(flatten(as_dict.values()))):
                return False
        return True


class InventoryRules(db.Model):
    __tablename__ = 'inventory_rules'
    id = db.Column(Integer, primary_key=True)

    parent_id = db.Column(Integer, db.ForeignKey(PropertiesRules.__tablename__ + '.id',
                                                 ondelete='CASCADE'),
                          nullable=False)

    price_start = db.Column(Integer, nullable=False)
    price_end = db.Column(Integer, nullable=False)

    fireplace = db.Column(Integer)
    full_bath = db.Column(Integer)
    half_bath = db.Column(Integer)
    gla_sqft = db.Column(Integer)
    under_air_gla_sqft = db.Column(Integer)

    # adjustment values for acres
    lot_sqft = db.Column(Float)

    garage = db.Column(Integer)
    bedrooms = db.Column(db.Integer)
    pool = db.Column(db.Integer)
    floor_height = db.Column(db.Integer)

    patio_type_prices = db.Column(ARRAY(Integer), server_default="{}")
    paving_type_prices = db.Column(ARRAY(Integer), server_default="{}")
    porch_type_prices = db.Column(ARRAY(Integer), server_default="{}")
    heat_type_prices = db.Column(ARRAY(Integer), server_default="{}")
    basement_prices = db.Column(ARRAY(Integer), server_default="{}")

    @property
    def lot_acre(self):
        return self.lot_sqft * SqftInAcre

    def basement_price(self, basement_type):
        """from Property.basement_type"""
        if not basement_type:
            return 0
        return self.basement_prices[int(basement_type)]


class SelectionRules(db.Model):
    id = db.Column(Integer, primary_key=True)
    proximity_range = db.Column(Numeric(precision=10, scale=3), nullable=True)
    parent_id = db.Column(Integer, db.ForeignKey(PropertiesRules.__tablename__ + '.id',
                                                 ondelete='CASCADE'),
                          nullable=False)

    sale_date_from = db.Column(db.Date(), nullable=True)
    sale_date_to = db.Column(db.Date(), nullable=True)

    # REQ: Ability to specify the range of from Subject Property - X% to +Y%
    percent_gla_lower = db.Column(Integer(), nullable=True)
    percent_gla_higher = db.Column(Integer(), nullable=True)
    # REQ: Ability to specify the range of from Subject Property - X% to +Y%
    percent_sale_lower = db.Column(Integer(), nullable=True)
    percent_sale_higher = db.Column(Integer(), nullable=True)

    percent_lot_size_lower = db.Column(db.Float, nullable=True)
    percent_lot_size_higher = db.Column(db.Float, nullable=True)

    same_property_class = db.Column(Boolean(), nullable=True)
    # REQ: Array of classes that can be considered equal
    same_one_family_types = db.Column(Boolean(), nullable=True)

    same_school_district = db.Column(Boolean(), nullable=True)
    same_town = db.Column(Boolean(), nullable=True)
    same_street = db.Column(Boolean(), nullable=True)
    same_property_style = db.Column(Boolean(), nullable=True)

    # for florida counties we may need to select comps based on the subject year
    # built within 10 years
    same_age = db.Column(Boolean())

    # if condo select comps only from same building
    same_building = db.Column(Boolean())

    # based on florida counties water_category
    prioritize_same_water_categories = db.Column(Boolean())

    def inherits_all_from_parent(self):
        as_dict = vars(self)
        as_dict.pop('_sa_instance_state')
        as_dict.pop('id')
        as_dict.pop('parent_id')
        return all(v is None for v in as_dict.values())


class SelectionRuleSchema(BaseSchema):
    class Meta:
        model = SelectionRules


class InventoryRuleSchema(BaseSchema):
    class Meta:
        model = InventoryRules


class RuleSetSchema(BaseSchema):
    class Meta:
        model = PropertiesRules

    last_updated = fields.DateTime(dump_only=True)
    selection_rules = Nested(SelectionRuleSchema(), many=False)
    inventory_rules = Nested(InventoryRuleSchema(), many=True)


class AdjustmentSchema(Schema):
    name = fields.String()
    rule_field = fields.String()
    property_field = fields.String()
    key = fields.String()
