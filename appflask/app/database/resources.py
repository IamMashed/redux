import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
import simplejson as json
from flask import request, Response, jsonify
from flask_login import current_user
from flask_restful import Resource
from flask_security.utils import hash_password
from werkzeug.exceptions import HTTPException

from app import db, TOWNS
from app.database.models import Property, User, Assessment, Role
from app.database.models.assessment import AssessmentModelSchema
from app.database.models.files import DataMappers, DataMapperSchema
from app.database.models.property import BasePropertyModelSchema, PropertyModelSchema, PropertyCounty, \
    PropertyCountySchema
from app.database.models.user import UserSchema, Permission, RoleSchema
from app.routing import Domain
from app.routing.decorators import permission_required
from app.routing.errors import forbidden, not_found, bad_request, server_error
from app.routing.services import PropertyService, PhotoService, HearingService
from app.utils.comp_utils import get_whitelisted
from app.utils.constants import County, NASSAU_VILLAGES


class PropertiesApi(Resource):
    SEARCH_LIMIT = 100

    def get(self):
        """
        Get properties by filter criteria
        """

        if request.args.get('county') not in Domain.get_allowed_counties(domain=request.headers['Host']):
            return not_found('Requested county does not exist')

        args = request.args.to_dict()
        args['limit'] = args.get('limit') or self.SEARCH_LIMIT

        # search properties in property_overridden table first
        args['ignore_address_tail'] = True
        properties = PropertyService.search_properties(args.copy(), model=Property)

        # make comps photos urls
        properties = [PhotoService.make_all_photos_urls(o) for o in properties]

        # filter out non whitelisted
        properties = get_whitelisted(properties)
        # serialize query objects
        return jsonify(BasePropertyModelSchema(many=True).dump(properties[:self.SEARCH_LIMIT]))


class PropertyApi(Resource):
    # add more fields, can be overridden
    overridden_inventory_fields = [
        'gla_sqft', 'lot_size', 'full_baths', 'half_baths', 'bedrooms', 'pool', 'patio_type', 'paving_type',
        'porch_type', 'heat_type', 'garages', 'basement_type',
    ]

    def _get_inventory_mappings(self, data):
        """
        Get inventory fields mapping, that allowed to be overridden
        """
        mappings = {}
        for key, value in data.items():
            # map attribute, if one in the hard coded inventory list
            if key in self.overridden_inventory_fields:
                mappings[key] = value
        return mappings

    def get(self, property_id):
        """
        Get specific property data
        GET Params:
            :original: Whether return original property data or last updated
        """
        # whether return original property data or last updated
        original = request.args.get('original', False, type=bool)

        prop = PropertyService.get_property(property_id, original=original)
        dump = json.dumps(PropertyModelSchema().dump(prop))
        return Response(dump, mimetype="application/json", status=200)

    def put(self, property_id):
        """
        Update specific property
        When the data of the property is updated, first save the original data into PropertyOriginal model
        and then update the Property table.
        """
        # ensure that original data saved first
        PropertyService.backup_original_property(property_id)

        json_data = request.get_json()
        json_data['id'] = property_id

        # filter out fields to ensure that only inventory fields can be updated
        inventory_fields = self._get_inventory_mappings(json_data)
        db.session.query(Property).filter(Property.id == property_id).update(
            inventory_fields,
            synchronize_session=False
        )
        db.session.commit()

        updated_prop = db.session.query(Property).filter_by(id=property_id).one()
        return Response(json.dumps(PropertyModelSchema().dump(updated_prop)), mimetype="application/json", status=200)

    def delete(self, property_id):
        """
        Restore last updated property to original data
        """

        if PropertyService.original_property_exists(property_id):
            last_updated = db.session.query(Property).filter_by(id=property_id).first_or_404()
            PropertyService.override_property_from_original(last_updated)

            return Response(
                response=json.dumps(PropertyModelSchema().dump(last_updated)),
                mimetype="application/json",
                status=200
            )


class AssessmentsApi(Resource):
    DEFAULT_LIMIT = 100

    def get(self, assessment_date_id):
        """
        Get list of assessments by 'assessment_date_id' and optional get parameter 'property_id'
        """
        property_id = request.args.get('property_id', type=int)
        limit = request.args.get('limit', type=int) or self.DEFAULT_LIMIT
        if property_id:
            assessments = db.session.query(Assessment).filter(
                Assessment.property_id == property_id,
                Assessment.assessment_id == assessment_date_id
            ).all()

        else:
            assessments = db.session.query(Assessment).filter(
                Assessment.assessment_id == assessment_date_id
            ).limit(limit).all()
        return jsonify(AssessmentModelSchema().dump(assessments, many=True))


class AssessmentApi(Resource):
    def get(self, assessment_id):
        """
        Get specific assessment
        """
        assessment = Assessment.query.get(assessment_id)
        return jsonify(AssessmentModelSchema().dump(assessment))

    @permission_required(Permission.ADMIN)
    def put(self, assessment_id):
        """
        Update specific assessment
        """
        data = request.get_json()

        # allow to modify only 'override_value'
        assessment = Assessment.query.get(assessment_id)
        assessment.override_value = data.get('override_value', None)

        db.session.add(assessment)
        db.session.commit()

        return jsonify(AssessmentModelSchema().dump(assessment))


class CountiesApi(Resource):
    def get(self):
        """
        Get all unique counties.
        """

        counties = db.session.query(PropertyCounty).filter(
            PropertyCounty.id.in_(Domain.get_allowed_counties(domain=request.headers['Host']))
        ).all()

        return jsonify(PropertyCountySchema().dump(counties, many=True))


class VillagesApi(Resource):
    def get(self, county_name):
        """ Get all nassau villages """

        villages = {
            k: p.village for k, p in enumerate(Property.query.filter_by(
                county=county_name
            ).distinct(Property.village).order_by(Property.village.asc())) if p.village is not None
        }

        if county_name == County.NASSAU:
            nv = dict(NASSAU_VILLAGES)
            villages = {k: nv.get(v) for k, v in villages.items()}

        return Response(json.dumps(villages), mimetype="application/json", status=200)


class TownshipsApi(Resource):
    def get(self, county_name):
        """
        Get all Townships by county_name
        :param county_name: The county name
        """
        # towns = [p.town for p in Property.query.filter_by(county=county_name).distinct(Property.town)]
        # return jsonify(towns)

        # TODO: using hardcoded data from 'TOWNS'
        if county_name in [County.NASSAU, County.SUFFOLK]:
            return Response(json.dumps(TOWNS[county_name]), mimetype="application/json", status=200)

        return Response(json.dumps({}), mimetype="application/json", status=200)


class UsersApi(Resource):
    def get(self):
        """
        Get list of users
        """
        users = User.query.all()
        return Response(
            response=json.dumps(UserSchema().dump(users, many=True)),
            mimetype="application/json",
            status=200
        )

    def post(self):
        """
        Create a new user
        """
        json_data = request.get_json()
        json_data['password'] = hash_password(json_data.get('password'))
        errors = UserSchema().validate(json_data)

        # respond validation errors
        if errors:
            return bad_request(errors)

        user_name = json_data.get('username')
        user = User.get_by(username=user_name)
        if user:
            return bad_request('{} already exists'.format(user_name))

        try:
            new_user = UserSchema(exclude=('id',)).load(json_data)
            new_user.save()
            return jsonify(UserSchema().dump(new_user))
        except Exception as e:
            return server_error(e.args)


class UserApi(Resource):
    def get(self, user_id):
        """
        Get specific user
        :param user_id: The user id
        """
        user = User.get(user_id)
        if not user:
            return not_found("User with id={} was not found".format(user_id))
        return jsonify(UserSchema().dump(user, many=False))

    def put(self, user_id):
        """
        Update specific user
        :param user_id: The user id
        """
        user = User.get(user_id)
        if not user:
            return not_found("User with id={} was not found".format(user_id))

        json_data = request.get_json()
        json_data['id'] = user_id

        password = json_data.get('password')
        json_data['password'] = hash_password(password) if password else user.password

        # validate
        errors = UserSchema().validate(json_data)
        if errors:
            return bad_request(errors)

        try:
            updated_user = UserSchema().load(json_data)
            updated_user.save()
            return jsonify(UserSchema().dump(updated_user))
        except Exception as e:
            return server_error(e.args)

    def delete(self, user_id):
        """
        Delete specific user
        :param user_id: The user id
        """
        try:
            user = User.get_or_404(user_id)
            user.delete()
            return jsonify({
                'status': True
            })
        except HTTPException:
            return not_found("User with id={} was not found".format(user_id))


class RolesApi(Resource):
    def get(self):
        roles = Role.query.all()
        return jsonify(RoleSchema().dump(roles, many=True))


class UserAuthApi(Resource):
    def get(self):
        """
        Get current user
        """
        if current_user.is_anonymous:
            return forbidden('Unauthenticated user')
        response = jsonify({
            'user_id': current_user.id,
            'user_role': current_user.role.name,
            'user_permissions': current_user.role.permissions,
            'domain': request.headers['Host'],
            'permissions': {
                'VIEW': 1,
                'EDIT': 2,
                'CASE_MANAGEMENT': 4,
                'SINGLE_CMA': 8,
                'MASS_CMA': 16,
                'ADMIN': 32,
            }
        })
        response.status_code = 200
        return response


class DataMappersApi(Resource):
    def get(self):
        """
        Get all data mappers
        """
        data_mappers = DataMappers.query.all()
        return jsonify(DataMapperSchema().dump(data_mappers, many=True))


class DataMapperApi(Resource):
    def get(self, name):
        """
        Get specific data mapper by name
        """
        data_mapper = DataMappers.get_or_404(name)
        return jsonify(DataMapperSchema().dump(data_mapper, many=False))

    def put(self, name):
        """
        Update specific data mapper by name
        """
        try:
            json_data = request.get_json()
            json_data['name'] = name
            json_data['updated_at'] = str(datetime.now())
            updated_data_mapper = DataMapperSchema(exclude=('created_at', )).load(json_data)
            updated_data_mapper.save()

            return jsonify(DataMapperSchema().dump(updated_data_mapper))
        except Exception as e:
            logging.error(e.args)
            import traceback
            return server_error(traceback.format_exc())


class PetitionFileUploadApi(Resource):
    def post(self):
        # get petition file need to upload
        petition_file = request.files.get('petition_file', None)

        # validate petition file is not None
        if not petition_file:
            response = jsonify(error="No petition file found")
            response.status_code = 500
            return response

        # validate supported file extension
        file_name = petition_file.filename
        if Path(file_name).suffix.lower() not in ('.xls', '.xlsx'):
            response = jsonify(error="Not supported file format")
            response.status_code = 500
            return response

        # get petition file data mapper
        data_mapper = DataMappers.get_by(name=DataMappers.PETITION)
        fields = data_mapper.clean_fields()

        # validate required columns
        for key in DataMappers.required_columns:
            if key not in fields.keys():
                return jsonify(error=f"Missing required column: {key}")

        try:
            # get columns to read from uploading file
            col_names = [v for k, v in fields.items()]

            # read all columns as 'str' type
            dtypes = {col: str for col in col_names if fields['apn'] == col}

            # read file headers
            headers = pd.read_excel(petition_file, nrows=0).columns.tolist()

            # read uploading file
            df = pd.read_excel(petition_file, usecols=headers, dtype=dtypes)

            # remove '\xa0' from column names
            df.rename(lambda col: col.replace('\xa0', ''), axis='columns', inplace=True)

            # remove useless columns coming with input file
            df = df[col_names]

            # create rename columns mapper
            rename_columns = {v: k for k, v in fields.items()}

            # rename columns
            df.rename(columns=rename_columns, inplace=True)

            # replace null values
            df.fillna('', inplace=True)

            # read and parse petition file data
            df = df.apply(HearingService.parse_petition_row, axis=1)

            # persist petition data
            HearingService.persist_petition_data(df)

            return jsonify(success=True)
        except Exception as e:
            import traceback
            logging.error(e.args)
            logging.error(traceback.format_exc())

            response = jsonify(error=e.args)
            response.status_code = 500

            return response
