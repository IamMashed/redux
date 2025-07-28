from marshmallow import Schema, fields
from marshmallow.fields import Nested

from app import db
from app.case_management.mixins import BaseMixin
from app.database.models.assessment import AssessmentModelSchema
from app.database.models.property import SubjectPropertySchema, ComparativePropertySchema
from app.rules.models import RuleSetSchema
from app.settings.models import BaseSchema


class SingleCMAWorkups(db.Model, BaseMixin):
    __tablename__ = 'single_sma_workups'

    id = db.Column(db.Integer, primary_key=True)
    case_property_id = db.Column(
        db.Integer,
        db.ForeignKey('case_property.id', name="fk_single_cma_workups_case_property_id")
    )
    case_property = db.relationship('CaseProperty', backref='workups')

    report_file_id = db.Column(
        db.Integer,
        db.ForeignKey('files.id', name="fk_single_sma_workups_report_file_id"),
    )
    good_bad_report_file_id = db.Column(
        db.Integer,
        db.ForeignKey('files.id', name="fk_single_sma_workups_good_bad_report_file_id"),
    )
    report_file = db.relationship("Files", foreign_keys=[report_file_id], uselist=False, cascade="all,delete")
    good_bad_report_file = db.relationship("Files", foreign_keys=[good_bad_report_file_id],
                                           uselist=False, cascade="all,delete")

    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)
    cma_payload = db.Column(db.JSON)

    @classmethod
    def get_last_workup(cls, case_property_id):
        """
        Get case last workup
        """
        last_workup = db.session.query(SingleCMAWorkups).filter(
            SingleCMAWorkups.case_property_id == case_property_id
        ).order_by(SingleCMAWorkups.created_at.desc()).first()
        return last_workup

    @classmethod
    def get_primary_workup(cls, case_property_id):
        """
        Get case primary workup
        """
        primary_workup = SingleCMAWorkups.get_by(case_property_id=case_property_id, is_primary=True)

        # primary workup must exists but if for some reason no primary workup,
        # to be sure system is not broke return the last workup
        if not primary_workup:
            primary_workup = cls.get_last_workup(case_property_id)

        return primary_workup


class SingleCMASchema(Schema):
    """
    Define a schema of Single CMA computation result
    """
    subject = Nested(SubjectPropertySchema(), many=False)
    assessment = Nested(AssessmentModelSchema(), many=False)
    all_comps = Nested(ComparativePropertySchema(), many=True)
    average_ranges = fields.Dict(dump_only=True)
    assessment_results = fields.Dict(dump_only=True)
    assessment_date_id = fields.Integer(dump_only=True, allow_none=True)
    rule_set = Nested(RuleSetSchema(), many=False, load_only=True)


class SingleCMAWorkupsSchema(BaseSchema):
    class Meta:
        model = SingleCMAWorkups
