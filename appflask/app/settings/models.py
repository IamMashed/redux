from collections import OrderedDict

from marshmallow import EXCLUDE, fields, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchemaOpts, SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import Integer, String, Numeric

from app import db
from app.utils.constants import County

ASSESSMENT_TYPES = OrderedDict([
    (1, 'final'),
    (2, 'tent'),
    (3, 'school')
])


# County settings map
GLOBAL_SETTINGS_SAMPLE = {
    County.NASSAU: {
        "pdf_header": "PROPERTY TAX REDUCTION CONSULTANTS 125 JERICHO TPKE, SUITE 500, "
                      "JERICHO NY 11753 516-474-0654 516-484-2565 (FAX)",
        "logo": "logo.jpg",
        "good_comps_count": 14,
        "bad_comps_count": 222,
        "all_comps_count": 111,
        "mass_cma_enable": True
    },
    County.SUFFOLK: {
        "pdf_header": "The suffolk header 1",
        "logo": "suffolk.png",
        "good_comps_count": 2,
        "all_comps_count": 16,
    }
}


class CustomInteger(fields.Field):
    """
    Field that deserialize empty string to None.
    """

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            if value == '':
                return None
            return int(value)
        except ValueError:
            raise ValidationError('Invalid int value')


class BaseOpts(SQLAlchemyAutoSchemaOpts):
    """
    Base schema configurations:
        * session
        * unknown
    """
    def __init__(self, meta, ordered=False):
        if not hasattr(meta, "sqla_session"):
            meta.sqla_session = db.session
        if not hasattr(meta, "unknown"):
            meta.unknown = EXCLUDE
        if not hasattr(meta, "load_instance"):
            meta.load_instance = True
        if not hasattr(meta, "include_fk"):
            meta.include_fk = True
        super(BaseOpts, self).__init__(meta, ordered=ordered)


class BaseSchema(SQLAlchemyAutoSchema):
    """
    Base configured schema class
    """
    OPTIONS_CLASS = BaseOpts


class Ratio(db.Model):
    __tablename__ = 'ratios'
    id = db.Column(Integer, primary_key=True)
    ratios_settings_id = db.Column(db.Integer, db.ForeignKey('settings_ratios.id'),
                                   nullable=False)
    year = db.Column(Integer, nullable=False)
    value = db.Column(Numeric(precision=17, scale=7), nullable=True, default=None)

    @classmethod
    def get_ratio(cls, year, county, town=None):
        q = db.session.query(cls).join(
            RatiosSettings,
            Ratio.ratios_settings_id == RatiosSettings.id
        ).filter(
            Ratio.year == year, RatiosSettings.county == county
        )
        if county == County.SUFFOLK:
            q = q.filter(RatiosSettings.name == town)
        f = q.first()
        return f.value if f else 1


class RatiosSettings(db.Model):
    __tablename__ = 'settings_ratios'
    id = db.Column(Integer, primary_key=True)

    county = db.Column(String(50), nullable=False)

    name = db.Column(String(100), nullable=False)
    description = db.Column(String(100), nullable=True, default=None)
    type = db.Column(db.String(100), nullable=True, default=None)

    ratios = db.relationship('Ratio', lazy='immediate', order_by="desc(Ratio.year)")

    @classmethod
    def add_nassau_codes(cls):
        from manage import app
        from app.database.models.property import NASSAU_VILLAGE_CODES
        with app.app_context():
            for code in NASSAU_VILLAGE_CODES:
                ratio_settings = RatiosSettings(county=County.NASSAU, name=code, description='', type='Village')
                db.session.add(ratio_settings)
                db.session.commit()


class RatioSchema(BaseSchema):
    class Meta:
        model = Ratio


class RatiosSettingsSchema(BaseSchema):

    ratios = Nested(RatioSchema, many=True)

    class Meta:
        model = RatiosSettings


class AssessmentDate(db.Model):
    __tablename__ = 'assessment_dates'
    __table_args__ = (
        # 'county' + 'assessment type' + 'valuation_date' must be unique
        db.UniqueConstraint('county', 'assessment_type', 'valuation_date', name='uc_county_valuation_date_type'),
    )
    id = db.Column(db.Integer, primary_key=True)
    county = db.Column(db.String, nullable=False)

    # assessment type
    assessment_type = db.Column(db.Integer, nullable=False)

    # assessment date name, defined by client
    assessment_name = db.Column(db.String, nullable=True)

    # used in CMA logic
    valuation_date = db.Column(db.Date, nullable=False)

    release_date = db.Column(db.Date)

    # used to pick the correct Ratio from Ratios Settings
    tax_year = db.Column(db.Integer, nullable=False)

    # assessment files
    # assessment_file = db.Column(db.String, nullable=False)
    files = db.relationship("AssessmentFile", lazy="joined", cascade="all, delete-orphan")

    @classmethod
    def select_field_choices(cls, county=None):
        assessment_dates = cls.query
        if county:
            assessment_dates = assessment_dates.filter_by(county=county)
        all_ = assessment_dates.all()
        choices = [
            (str(date.id),
             f'{date.valuation_date.year}/{date.valuation_date.month} {ASSESSMENT_TYPES.get(date.assessment_type)}')
            for date in all_]
        return choices


class AssessmentFile(db.Model):
    __tablename__ = 'assessment_files'

    id = db.Column(db.Integer, primary_key=True)
    assessment_date_id = db.Column(db.Integer, db.ForeignKey('assessment_dates.id'), nullable=False)
    file_name = db.Column(db.String, nullable=False)


class TimeAdjustmentValue(db.Model):
    __tablename__ = 'time_adjustments'
    __table_args__ = (db.UniqueConstraint('county', 'year', 'month', name='unique_county_year_month'),)

    id = db.Column(db.Integer, primary_key=True)
    county = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    value = db.Column(db.Float)


class GlobalSetting(db.Model):
    __tablename__ = 'settings_global'
    __table_args__ = (db.UniqueConstraint('county', name='uc_county'),)

    id = db.Column(db.Integer, primary_key=True)
    county = db.Column(db.String, nullable=True)
    settings = db.Column(JSONB, nullable=False, server_default='{}')

    @staticmethod
    def init_settings():
        """
        Initialize global settings
        """
        for county in County.get_counties():
            obj = db.session.query(GlobalSetting).filter_by(county=county).first()
            if obj is None:
                obj = GlobalSetting(county=county, settings={})
                db.session.add(obj)
        db.session.commit()

    @staticmethod
    def insert_sample_settings():
        for county in GLOBAL_SETTINGS_SAMPLE.keys():
            obj = db.session.query(GlobalSetting).filter_by(county=county).first()
            if obj is None:
                obj = GlobalSetting(county=county, settings={})
            else:
                obj.settings = GLOBAL_SETTINGS_SAMPLE[county]
            db.session.add(obj)
        db.session.commit()

    @classmethod
    def get_value(cls, key: str, county=None):
        """
        Get global setting value
        """
        obj = db.session.query(GlobalSetting).filter_by(county=county).first()
        if obj is None:
            return None

        return obj.settings.get(key, None)


class AssessmentFileSchema(BaseSchema):
    class Meta:
        model = AssessmentFile


class AssessmentDateSchema(BaseSchema):
    class Meta:
        model = AssessmentDate
    files = Nested(AssessmentFileSchema(), many=True)


class TimeAdjustmentApiSchema(BaseSchema):
    class Meta:
        model = TimeAdjustmentValue


class GlobalSettingSchema(BaseSchema):
    class Meta:
        model = GlobalSetting
