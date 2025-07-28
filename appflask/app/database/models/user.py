import json
import uuid
from collections import namedtuple
from datetime import datetime
from time import time
# import pandas as pd

from flask import current_app
from flask_login import AnonymousUserMixin
from flask_security import UserMixin, RoleMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from marshmallow import fields
from marshmallow_sqlalchemy.fields import Nested

from app import db
from app.case_management.mixins import BaseMixin
from app.database.models import Assessment
from app.database.models.cma import CmaTask, CmaResult
from app.database.models.property import Property, TOWNS
from app.rules.controllers import RulesController
from app.rules.models import PropertiesRules
from app.settings.models import AssessmentDate, Ratio, TimeAdjustmentValue, BaseSchema
from app.utils.comp_utils import get_whitelisted
from app.utils.constants import get_town_name, get_town_code, County
from config import MASS_CMA_LIMIT, MASS_CMA_CHUNK_SIZE, ROLE_GUEST, ROLE_MEMBER, ROLE_ADMIN


class Permission:
    """
    Role permission class.
    Each permission must describe a numerical series as 2 in degree of N, where N=(0,1,...)
    to exclude permission overriding
    """

    VIEW = 1
    EDIT = 2
    CASE_MANAGEMENT = 4
    SINGLE_CMA = 8
    MASS_CMA = 16
    ADMIN = 32


class Role(db.Model, RoleMixin, BaseMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        """
        Insert roles and role permissions.
        """
        roles = {
            ROLE_GUEST: [Permission.VIEW],
            ROLE_MEMBER: [Permission.VIEW, Permission.CASE_MANAGEMENT, Permission.SINGLE_CMA],
            ROLE_ADMIN: [
                Permission.VIEW, Permission.EDIT, Permission.CASE_MANAGEMENT, Permission.SINGLE_CMA,
                Permission.MASS_CMA, Permission.ADMIN
            ]
        }
        default_role = ROLE_MEMBER
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r, description=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        """
        Add permission
        :param perm: The permission weight
        """
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        """
        Remove permission
        :param perm: The permission weight
        """
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        """
        Reset permissions
        """
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm


class User(db.Model, UserMixin, BaseMixin):
    __tablename__ = 'users'
    __table_args__ = (
        db.UniqueConstraint('username', name='uc_users_username'),
    )

    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #     self.password = hash_password(kwargs.get('password'))

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    username = db.Column(db.String(50))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    # roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    tasks = db.relationship('CmaTask', backref='user', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    mass_cma_filter = db.relationship('UserMassCmaFilter', backref='user', uselist=False)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return None
        return User.query.get(data['id'])

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def launch_task(self, name, description, county, village, assessment_date_id, assessment_stage,
                    sale_dates_from, sale_dates_to):
        """
        village: can also refer to the township i.e in case for suffolk county
        """

        props = Property.query.with_entities(Property.id,
                                             Property.county,
                                             Property.property_class,
                                             Property.property_class_type,
                                             Property.is_condo).filter_by(county=county).filter(
            Property.gla_sqft.isnot(None))

        if assessment_stage:
            props = props.filter(Property.assessment_stage == assessment_stage)

        town = None
        if county == County.NASSAU:
            if village == 'All Villages':
                props = props.filter(Property.village.isnot(None))
            if village not in ('Whole County', 'None'):
                props = props.filter(Property.village == village)
        else:  # for the rest counties
            if village not in ('Whole County', 'None'):
                town = get_town_code(TOWNS, county, village)
                props = props.filter(Property.town == town)

        if MASS_CMA_LIMIT:  # defining limit for development
            props = props.limit(MASS_CMA_LIMIT).all()
        else:
            props = props.all()

        # allow only whitelisted properties for mass cma
        PropertyTuple = namedtuple('PropertyTuple', ['id', 'county',
                                                     'property_class', 'property_class_type', 'is_condo'])
        transformed_props = [PropertyTuple(*prop) for prop in props]
        props = get_whitelisted(transformed_props)
        props = [prop.id for prop in props]

        # wrong_ids_file = DATA_IMPORT / 'src' / 'miamidade' / 'miamidade_wrong_cma_ids.csv'
        # df = pd.read_csv(wrong_ids_file)
        # props = list(df['property_id'])

        job_id = uuid.uuid4().hex
        task = CmaTask(id=job_id,
                       county_name=county,
                       description=description,
                       total=len(props),
                       user=self,
                       task_ts=datetime.now(),
                       assessment_date_id=int(assessment_date_id),
                       sale_dates_from=sale_dates_from,
                       sale_dates_to=sale_dates_to)
        task.complete = True if not props else False
        db.session.add(task)
        db.session.commit()

        # query constants
        assessment_date = AssessmentDate.query.get(assessment_date_id)

        tax_year = assessment_date.tax_year
        assessment_ratio = Ratio.get_ratio(tax_year, county, town=town)

        time_adjustments = TimeAdjustmentValue.query.filter(
            TimeAdjustmentValue.county == county).all()
        properties_rules = PropertiesRules.load_rules(
            county,
            town=None,
            year=assessment_date.tax_year)
        rules_controller = RulesController(properties_rules,
                                           time_adjustments=time_adjustments,
                                           valuation_date=assessment_date.valuation_date)

        n = int(MASS_CMA_CHUNK_SIZE)
        print(f'Starting mass cma with limit {MASS_CMA_LIMIT} and chunk size {n}')
        chunks = (props[i * n:(i + 1) * n] for i in range((len(props) + n - 1) // n))
        for chunk in chunks:
            current_app.task_queue.enqueue('app.tasks.' + name,
                                           chunk,
                                           job_id,
                                           sale_dates_from,
                                           sale_dates_to,
                                           assessment_date,
                                           assessment_ratio,
                                           rules_controller,
                                           job_timeout=2500)
        return task

    def get_tasks_in_progress(self):
        # TODO: who is allowed to start a task? Can another user start suffolk while nassau is running?
        return CmaTask.query.filter_by(user=self, complete=False).all()

    def get_task_in_progress(self, name):
        return CmaTask.query.filter_by(county_name=name, user=self, complete=False).first()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    def apply_mass_cma_filter(self, q, assessment_ratio, form=None):
        f = self.mass_cma_filter
        if f.county:
            q = q.filter(Property.county == f.county)
            if form:
                form.county.data = f.county

        if f.town:
            q = q.filter(Property.town == f.town)
            if form:
                form.town.data = get_town_name(TOWNS, f.county, f.town)

        if f.village:
            if f.village == 'No Village':
                q = q.filter(Property.village.is_(None))
            elif f.village == 'None':
                pass
            else:
                q = q.filter(Property.village == f.village)
            if form:
                form.village.data = f.village

        if f.section:
            q = q.filter(Property.section == f.section)
            if form:
                form.section.data = f.section
        if f.block:
            q = q.filter(Property.block == f.block)
            if form:
                form.block.data = f.block
        if f.lot:
            q = q.filter(Property.lot == f.lot)
            if form:
                form.lot.data = f.lot
        if f.street:
            q = q.filter(Property.street.ilike(f.street))
            if form:
                form.street.data = f.street
        if f.number:
            q = q.filter(Property.number == f.number)
            if form:
                form.number.data = f.number
        if f.school_district:
            q = q.filter(Property.school_district == f.school_district)
            if form:
                form.school_district.data = f.school_district
        if f.saving_min:
            q = q.filter((Assessment.assessment_value - CmaResult.computed_cma) >=
                         f.saving_min)
            if form:
                form.saving_min.data = f.saving_min
        if f.saving_max:
            q = q.filter((Assessment.assessment_value - CmaResult.computed_cma) <=
                         f.saving_max)
            if form:
                form.saving_max.data = f.saving_max
        if f.market_value_min:
            q = q.filter((Assessment.value / assessment_ratio) >=
                         int(f.market_value_min))
            if form:
                form.market_value_min.data = f.market_value_min
        if f.market_value_max:
            q = q.filter((Assessment.value / assessment_ratio) <=
                         int(f.market_value_max))
            if form:
                form.market_value_max.data = f.market_value_max
        return q


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))


class UserMassCmaFilter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    county = db.Column(db.String)
    town = db.Column(db.String)
    village = db.Column(db.String)
    section = db.Column(db.String)
    block = db.Column(db.String)
    lot = db.Column(db.String)
    street = db.Column(db.String)
    number = db.Column(db.String)
    school_district = db.Column(db.Integer)
    saving_min = db.Column(db.Integer)
    saving_max = db.Column(db.Integer)
    market_value_min = db.Column(db.Integer)
    market_value_max = db.Column(db.Integer)


class RoleSchema(BaseSchema):
    class Meta:
        model = Role


class UserSchema(BaseSchema):
    class Meta:
        model = User
        load_only = ('password',)

    password = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.String(default='')

    role_id = fields.Integer(required=True)
    role = Nested(RoleSchema(), many=False, dump_only=True)
