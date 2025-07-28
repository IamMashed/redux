import datetime

from app import db
from app.database.models.property import Property


class CmaTask(db.Model):
    """
    CMA task, initial version
    can have CmaResults related to the task

    * for background processing states can be added (New, Processing, Complete, Failed)
    """
    id = db.Column(db.String, primary_key=True)
    # task timestamp
    task_ts = db.Column(db.DateTime, default=datetime.datetime.now())
    task_complete_ts = db.Column(db.DateTime)
    county_name = db.Column(db.String, index=True)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    total = db.Column(db.Integer)
    complete = db.Column(db.Boolean, default=False)
    assessment_date_id = db.Column(db.Integer, db.ForeignKey('assessment_dates.id'))
    sale_dates_from = db.Column(db.Date)
    sale_dates_to = db.Column(db.Date)
    results = db.relationship('CmaResult', backref='task', lazy='dynamic')
    assessment_date = db.relationship('AssessmentDate',
                                      backref='cma_task',
                                      lazy='joined',
                                      uselist=False)

    def get_progress(self):
        percent = round(self.results.count() / self.total * 100, 1) if self.total else 0
        return f'{percent} %'

    @classmethod
    def get_task_in_progress(cls):
        return cls.query.filter_by(complete=False).first()


class CmaResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String, db.ForeignKey(CmaTask.__tablename__ + '.id'), nullable=False)
    property_id = db.Column(
        db.Integer,
        db.ForeignKey(Property.__tablename__ + '.id', name='cma_result_property_id_fkey'),
        nullable=False,
        onupdate='CASCADE'
    )
    subject_sale = db.Column(db.Integer)
    subject_sale_price = db.Column(db.Integer)
    computed_cma = db.Column(db.Integer, nullable=True)  # computed_cma_small (1-4)
    computed_cma_medium = db.Column(db.Integer, nullable=True)
    computed_cma_high = db.Column(db.Integer, nullable=True)
    computed_cma_good_small = db.Column(db.Integer, nullable=True)
    computed_cma_good_medium = db.Column(db.Integer, nullable=True)
    computed_cma_good_high = db.Column(db.Integer, nullable=True)
    total_good_comps = db.Column(db.Integer, nullable=True)
    total_all_comps = db.Column(db.Integer, nullable=True)
    error = db.Column(db.String)
