from marshmallow import fields, Schema
from marshmallow_sqlalchemy.fields import Nested

from app import db
from app.database.models.mixin import UpsertMixin, ValidationMixin
from app.settings.models import BaseSchema, AssessmentDateSchema, CustomInteger

NASSAU_SWISS_CODES = [
    ('282223', 'Mineola'),
    ('282015', 'Hewlett Bay Park'),
    ('282019', 'Hewlett Neck'),
    ('282037', 'Woodsburgh'),
    ('282017', 'Hewlett Harbor'),
    ('282003', 'Cedarhurst'),
    ('282043', 'Atlantic Beach'),
    ('282033', 'Stewart Manor'),
    ('282221', 'Manor Haven'),
    ('282207', 'Flower Hill'),
    ('282039', 'Mineola'),
    ('280600', 'Glen Cove, County Roll'),
    ('2806', 'Glen Cove, County Roll'),
    ('282419', 'Oyster Bay Cove'),
    ('282489', 'Oyster Bay'),
    ('282421', 'MatineCock'),
    ('282417', 'Massapequa Park'),
    ('282407', 'Cove Neck'),
    ('282427', 'Upper Brookville'),
    ('282245', 'Roslyn Harbor'),
    ('282433', 'Roslyn Harbor'),
    ('282229', 'North Hills'),
    ('282408', 'East Hills'),
    ('282425', 'Mill Neck'),
    ('282225', 'Munsey Park'),
    ('282401', 'Bayville'),
    ('281000', 'Long Beach, County Roll'),
    ('282237', 'Plandome Manor'),
    ('282413', 'Laurel Hollow'),
    ('282201', 'Bexter Estates'),
    ('282001', 'Bellerose'),
    ('282289', 'North Hempstead'),
    ('282233', 'Plandome'),
    ('282235', 'Plandome Heigths'),
    ('282405', 'Centre Island'),
    ('282261', '282261'),
    ('282005', 'East Rockaway'),
    ('282011', 'Garden City'),
    ('282029', 'Rockville Centre'),
    ('282021', 'Island Park'),
    ('282209', 'Great Neck'),
    ('282249', 'Saddle Rock'),
    ('282027', 'Malverne'),
    ('282007', 'Floral Park'),
    ('282239', 'Port Washington North'),
    ('282035', 'Valley Stream'),
    ('282257', 'Williston Park'),
    ('282423', 'Sea Cliff'),
    ('282203', 'East Hills'),
    ('282255', 'Westbury'),
    ('282025', 'Lynbrook'),
    ('282215', 'Kensington'),
    ('282013', 'Hempstead'),
    ('282089', 'Hempstead'),
    ('282231', 'Old Westbury'),
    ('282247', 'Russell Gardens'),
    ('282205', 'East Williston'),
    ('282217', 'Kings Point'),
    ('282227', 'New Hyde Park'),
    ('282041', 'New Hyde Park'),
    ('282241', 'Roslyn'),
    ('282211', 'Great Neck Estates'),
    ('282023', 'Lawrence'),
    ('282219', 'Lake Success'),
    ('282259', 'Floral Park'),
    ('282009', 'Freeport'),
    ('282213', 'Great Neck Plaza'),
    ('282253', 'Thomaston'),
    ('282415', 'Old Brookville'),
    ('282429', 'Muttontown'),
    ('282409', 'Farmingdale'),
    ('282243', 'Roslyn Estates'),
    ('282251', 'Sands Point'),
    ('282411', 'Lattingtown'),
    ('282403', 'Brookville'),
    ('282431', 'Old Westbury'),
    ('282031', 'South Floral Park')
]


class Assessment(db.Model, UpsertMixin):
    id = db.Column(db.Integer(), primary_key=True)

    # market value
    value = db.Column(db.Integer)

    # override market value
    market_value_override = db.Column(db.Integer)

    # assessment value
    assessment_value = db.Column(db.Integer)

    # override assessment value
    override_value = db.Column(db.Integer)

    assessment_date = db.relationship('AssessmentDate', backref='assessment')

    # reference to 'AssessmentDate' model
    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey('assessment_dates.id', name='assessment_assessment_dates_fkey'),
        index=True
    )

    # final, school or tent
    assessment_type = db.Column(db.String, default='final')

    FINAL = 'final'
    TENT = 'tent'

    # for assessment ratios
    swiss_code = db.Column(db.String)

    property_id = db.Column(
        db.Integer,
        db.ForeignKey('property.id', name='assessment_property_id_fkey', ondelete='cascade'),
        nullable=False,
        index=True
    )

    village_1 = db.Column(db.String)
    village_1_pct = db.Column(db.Float)
    village_2 = db.Column(db.String)
    village_2_pct = db.Column(db.Float)
    village_3 = db.Column(db.String)
    village_3_pct = db.Column(db.Float)

    @property
    def assessed_value(self):
        """
        Get correct assessment value
        """
        if self.override_value:
            return self.override_value

        return self.assessment_value


class AssessmentValidation(db.Model, ValidationMixin):
    id = db.Column(db.Integer, primary_key=True)
    apn = db.Column(db.String)
    county = db.Column(db.String)
    errors = db.Column(db.JSON)


"""
Six schemas in total based on the input types
TX451TWN#RS6400
Rectype 400 - Base Record
TX451TWN#RS6405
Rectype 405 - Total Tax Record
TX451TWN#RS6410
Rectype 410 - Exemption Records
TX451TWN#RS6420
Rectype 420 - Tax / Authority Records
TX451TWN#RS6430
Rectype 430 – Direct Assessment Records
TX451TWN#RS6440
Rectype 440 – Restored Tax Records
"""


class AssessmentSchema(Schema):
    apn = fields.String(required=True, data_key='parid')
    county = fields.String(missing='nassau')
    assessment_type = fields.String(data_key='assessment_type')
    swiss_code = fields.String(data_key='swiss_code')


class BaseRecord400Schema(AssessmentSchema):
    # crc1 = fields.Integer(data_key='crc1')
    # crc1_pct = fields.Float(data_key="crc1_pct")
    # crc2 = fields.Integer(data_key='crc2',
    #                       allow_none=True)
    # crc2_pct = fields.Float(data_key='crc2_pct',
    #                         allow_none=True)
    # crc3 = fields.Integer(data_key='crc3',
    #                       allow_none=True)
    # crc3_pct = fields.Float(data_key='crc3_pct',
    #                         allow_none=True)
    # crc4 = fields.Integer(data_key='crc4',
    #                       allow_none=True)
    # crc4_pct = fields.Float(data_key='crc4_pct',
    #                         allow_none=True)
    # crc5 = fields.Integer(data_key='crc5',
    #                       allow_none=True)
    # crc5_pct = fields.Float(data_key='crc5_pct',
    #                         allow_none=True)
    # crc6 = fields.Integer(data_key='crc6',
    #                       allow_none=True)
    # crc6_pct = fields.Float(data_key='crc6_pct',
    #                         allow_none=True)
    village_1 = fields.String(data_key='village_1',
                              allow_none=True)
    village_1_pct = fields.Float(data_key='village_1_pct',
                                 allow_none=True)
    village_2 = fields.String(data_key='village_2',
                              allow_none=True)
    village_2_pct = fields.Float(data_key='village_2_pct',
                                 allow_none=True)
    village_3 = fields.String(data_key='village_3',
                              allow_none=True)
    village_3_pct = fields.Float(data_key='village_3_pct',
                                 allow_none=True)
    owner_1 = fields.String(data_key='owner_1',
                            allow_none=True)
    owner_2 = fields.String(data_key='owner_2',
                            allow_none=True)
    # care_of = fields.String(data_key='care_of',
    #                         allow_none=True)
    # property_address = fields.String(data_key='property_address',
    #                                  allow_none=True)
    # property_address_2 = fields.String(data_key='property_address_2',
    #                                    allow_none=True)
    # lot = fields.String(data_key='lot',
    #                     allow_none=True)
    # property_desc = fields.Integer(data_key='property_desc',
    #                                allow_none=True)
    property_class = fields.Integer(data_key='property_class',
                                    allow_none=True)
    property_desc_2 = fields.String(data_key='property_desc_2',
                                    allow_none=True)
    # book = fields.Integer(data_key='book',
    #                       allow_none=True)
    # page = fields.Integer(data_key='page',
    #                       allow_none=True)
    # swiss_code = fields.Integer(data_key='swiss_code',
    #                             allow_none=True)
    # state_school_district = fields.Integer(
    #     data_key='state_school_district',
    #     allow_none=True)
    # roll_section = fields.Integer(data_key='roll_section',
    #                               allow_none=True)
    # excluded = fields.String(data_key='excluded',
    #                          allow_none=True)
    # prior_year_land_total = fields.Integer(
    #     data_key='prior_year_land_total',
    #     allow_none=True)
    # prior_year_total_assessment = fields.Integer(
    #     data_key='prior_year_total_assessment',
    #     allow_none=True)
    # total_land_assessment = fields.Integer(
    #     data_key='total_land_assessment',
    #     allow_none=True)
    value = fields.Integer(data_key='total_assessment',
                           allow_none=True)
    # total_market_value = fields.Integer(data_key='total_market_value',
    #                                     allow_none=True)
    # equalization_ratio = fields.Float(data_key='equalization_ratio',
    #                                   allow_none=True)
    # t_code_amount = fields.Integer(data_key='t_code_amount',
    #                                allow_none=True)
    # area_in_acres = fields.Float(data_key='acres',
    #                              allow_none=True)
    # area_in_square_foot = fields.Integer(data_key='square_foot',
    #                                      allow_none=True)

    owner_address_1 = fields.String(data_key='owner_address_1', allow_none=True)
    owner_address_2 = fields.String(data_key='owner_address_2', allow_none=True)
    owner_address_3 = fields.String(data_key='owner_address_3', allow_none=True)


class TotalTaxRecord405Schema(AssessmentSchema):
    tax_before_abatement = fields.Float(
        data_key="tax_before_abatement_or_star")
    abatement = fields.Float(data_key='abatement_or_star')
    first_half_tax = fields.Float(data_key='first_half_tax')
    second_half_tax = fields.Float(data_key='second_half_tax')
    total_tax = fields.Float(data_key='total_tax')
    exemption_count = fields.Integer(data_key='exemption_count')
    tax_or_authority_count = fields.Integer(
        data_key='tax_or_authority_count')
    direct_assessment_count = fields.Integer(
        data_key='direct_assessment')
    restored_tax_count = fields.Integer(data_key='restored_tax_count')


class Exemptions410Schema(AssessmentSchema):
    code = fields.Integer(data_key='code')
    description = fields.String(data_key='description')
    amount = fields.Integer(data_key='amount')
    computed_star = fields.Float(data_key='computed_star')
    capped_star = fields.Float(data_key='capped_star')
    actual_star = fields.Float(data_key='actual_star')
    star_difference = fields.Float(data_key='star_difference')


class TaxAuthority420Schema(AssessmentSchema):
    authority_code = fields.Integer(data_key='authority')
    authority_description = fields.String(
        data_key='authority_description')
    total_assessment = fields.Float(data_key='total_assessment')
    exempt_assessment = fields.Float(data_key='exempt_assessment')
    taxable_assessment = fields.Float(data_key='taxable_assessment')
    tax_rate = fields.Float(data_key='tax_rate')
    tax_amount = fields.Float(data_key='tax_amount')
    tax_district = fields.Float(data_key='tax_district',
                                allow_none=True)


class DirectAssessment430Schema(AssessmentSchema):
    project_number = fields.Integer(data_key='project_number')
    project_description = fields.String(data_key='project_description')
    tax_amount = fields.Float(data_key='tax_amount')


class RestoredTaxes440Schema(AssessmentSchema):
    exemption_code = fields.Integer(data_key='exemption_code')
    description = fields.String(data_key='description')
    tax_year = fields.Integer(data_key='tax_year')
    tax_amount = fields.Float(data_key='tax_amount')


class DisputedFund450Schema(AssessmentSchema):
    tax_year = fields.Integer(data_key='tax_year')
    daf_percentage = fields.Float(data_key='daf_percentage')
    daf_school_taxable = fields.Float(data_key='daf_school_taxable')
    daf_town_taxable = fields.Float(data_key='daf_town_taxable')
    daf_county_taxable = fields.Float(data_key='daf_county_taxable')
    daf_school_deduction = fields.Float(data_key='daf_school_deduction')
    daf_general_deduction = fields.Float(data_key='daf_general_deduction')
    daf_school_fund = fields.Float(data_key='daf_school_fund')
    daf_general_fund = fields.Float(data_key='daf_general_fund')


class DisputedFundSchema460Schema(AssessmentSchema):
    tax_year = fields.Integer(data_key='tax_year')
    star_amount = fields.Integer(data_key='star_amount')


class FloridaAssessmentSchema(Schema):
    apn = fields.String(required=True, data_key='apn')
    county = fields.String(data_key='county')
    swiss_code = fields.String(missing=None)

    value = fields.Float(data_key='value', missing=None)
    # assessment_date = fields.Date(data_key='assessment_date', missing=None)
    assessment_type = fields.String(data_key='assessment_type', missing=None)


class AssessmentModelSchema(BaseSchema):
    # user CustomInteger class that load empty string as None
    override_value = CustomInteger(allow_none=True)
    market_value_override = CustomInteger(allow_none=True)

    class Meta:
        model = Assessment

    assessment_date = Nested(AssessmentDateSchema(exclude=('files',)), many=False)
