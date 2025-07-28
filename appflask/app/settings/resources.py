import simplejson as json
from flask import Response, request, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from app import db
from app.database.models.user import Permission
from app.routing.decorators import permission_required, Domain
from app.settings.models import (
    RatiosSettings, RatiosSettingsSchema, Ratio,
    RatioSchema, AssessmentDate, AssessmentDateSchema,
    TimeAdjustmentValue, TimeAdjustmentApiSchema, GlobalSetting, GlobalSettingSchema)
from app.utils.constants import County


class RatiosSettingsResource(Resource):

    def get(self):
        schema = RatiosSettingsSchema(many=True)
        query = db.session.query(RatiosSettings)

        # check the request domain and filter counties accordingly
        query = query.filter(RatiosSettings.county.in_(Domain.get_allowed_counties(domain=request.headers['Host'])))
        objects = query.order_by(
            RatiosSettings.county.desc(),
            RatiosSettings.description.asc(),
        ).all()
        dump = json.dumps(schema.dump(objects))
        return Response(dump, mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def post(self):
        body = request.get_json()
        new_ratios = RatiosSettingsSchema().load(body)
        db.session.add(new_ratios)
        db.session.commit()
        return Response(json.dumps({'id': new_ratios.id}), mimetype="application/json", status=200)


class RatioResource(Resource):

    def get(self, id):
        return Response(RatioSchema().dump(db.session.query(Ratio)
                        .filter(Ratio.id == id).first()),
                        mimetype="application/json",
                        status=200)

    @permission_required(Permission.EDIT)
    def put(self, id):
        body = request.get_json()
        body['id'] = id
        return self._update(body)

    @permission_required(Permission.EDIT)
    def post(self):
        body = request.get_json()
        return self._update(body)

    def _update(self, json_data):
        print(json_data)
        ratio = RatioSchema().load(json_data)
        print(ratio)
        print(ratio.__dict__)
        db.session.add(ratio)
        db.session.commit()
        return Response(json.dumps({'id': ratio.id}), mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def delete(self, id):
        ratio = db.session.query(Ratio).filter(Ratio.id == id).first_or_404()
        db.session.delete(ratio)
        db.session.commit()
        return Response(json.dumps({'status': True}), mimetype="application/json", status=200)


class RatiosResource(Resource):

    @permission_required(Permission.EDIT)
    def post(self):
        return RatioResource()._update(request.get_json())


class AssessmentDatesApi(Resource):

    def get(self):
        """
        Get all assessment dates
        """
        query = AssessmentDate.query

        query = query.filter(AssessmentDate.county.in_(Domain.get_allowed_counties(domain=request.headers['Host'])))
        dates = query.all()
        dump = json.dumps(AssessmentDateSchema(many=True).dump(dates))

        return Response(dump, mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def post(self):
        new_date = AssessmentDateSchema().load(request.get_json(), session=db.session)
        db.session.add(new_date)
        db.session.commit()
        return Response(json.dumps({'id': new_date.id}), mimetype="application/json", status=200)


class AssessmentDateApi(Resource):
    def get(self, assmnt_id):
        """
        Get specific AssessmentDate
        """
        obj = AssessmentDate.query.filter_by(id=assmnt_id).first()
        dump = json.dumps(AssessmentDateSchema().dump(obj))
        return Response(dump, mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def put(self, assmnt_id):
        """
        Update specific AssessmentDate
        """
        json_data = request.get_json()
        json_data['id'] = assmnt_id

        assessment_date = AssessmentDateSchema().load(json_data, session=db.session)
        try:
            db.session.add(assessment_date)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            response = jsonify(error=e.args)
            response.status_code = 500
            return response
        return jsonify(AssessmentDateSchema().dump(assessment_date))

    @permission_required(Permission.EDIT)
    def delete(self, assmnt_id):
        """
        Delete specific AssessmentDate
        """
        assmnt_date = AssessmentDate.query.filter_by(id=assmnt_id).first_or_404()
        db.session.delete(assmnt_date)
        db.session.commit()
        return Response(json.dumps({'status': True}), mimetype="application/json", status=200)


class TimeAdjustmentsApi(Resource):

    def get(self):
        """
        Get all time adjustment values
        """
        query = TimeAdjustmentValue.query
        query = query.filter(TimeAdjustmentValue.county.in_(Domain.get_allowed_counties(request.headers['Host'])))

        # fetch all objects from database, sorted by county, year, month
        objects = query.order_by(TimeAdjustmentValue.county.asc(),
                                 TimeAdjustmentValue.year.asc(),
                                 TimeAdjustmentValue.month.asc()
                                 ).all()

        # serialize objects
        dump = json.dumps(TimeAdjustmentApiSchema(many=True).dump(objects))
        return Response(dump, mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def post(self):
        """
        Add time adjustment value
        """
        # get json data
        json_data = request.get_json()

        # validate data
        new_obj = TimeAdjustmentApiSchema().load(json_data, session=db.session)

        # push to db
        db.session.add(new_obj)
        db.session.commit()

        return Response(json.dumps({'id': new_obj.id}), mimetype="application/json", status=200)


class TimeAdjustmentApi(Resource):

    def get(self, adjmnt_id):
        """
        Get specific time adjustment value
        :param adjmnt_id: The id of time adjustment value
        """
        obj = TimeAdjustmentValue.query.filter_by(id=adjmnt_id).first_or_404()
        dump = json.dumps(TimeAdjustmentApiSchema().dump(obj))
        return Response(dump, mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def put(self, adjmnt_id):
        """
        Update specific time adjustment value
        :param adjmnt_id: The id of time adjustment value
        """
        json_data = request.get_json()
        json_data['id'] = adjmnt_id

        # deserialize object data
        new_obj = TimeAdjustmentApiSchema().load(json_data, session=db.session)

        # push to db
        db.session.add(new_obj)
        db.session.commit()

        return Response(json.dumps({'id': new_obj.id}), mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def delete(self, adjmnt_id):
        """
        Delete specific time adjustment value
        :param adjmnt_id: The id of time adjustment value
        """
        # get the object to delete
        obj = TimeAdjustmentValue.query.filter_by(id=adjmnt_id).first_or_404()

        db.session.delete(obj)
        db.session.commit()

        return Response(json.dumps({'status': True}), mimetype="application/json", status=200)


class GlobalSettingsApi(Resource):
    def get(self):
        """
        Get all global settings or get all county settings

        Request args:
        :arg county: The county to filter by
        """
        # get county name from the request
        county = request.args.get('county', None)

        # if invalid county name
        if county and county not in County.get_counties():
            response = jsonify(error="Invalid county name provided.")
            response.status_code = 500
            return response

        request_domain = request.headers['Host']
        if county:
            assert county in Domain.get_allowed_counties(domain=request_domain)
            objects = db.session.query(GlobalSetting).filter_by(county=county).all()
        else:
            query = db.session.query(GlobalSetting)
            query = query.filter(GlobalSetting.county.in_(Domain.get_allowed_counties(domain=request_domain)))
            objects = query.all()
        dump = json.dumps(GlobalSettingSchema().dump(objects, many=True))

        return Response(dump, mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def post(self):
        """
        Add county specific global settings
        """
        json_data = request.get_json()
        county = json_data.get('county', None)
        try:
            if county not in (County.get_counties() or None):
                raise AttributeError("Invalid county name")

            new_settings = GlobalSettingSchema().load(json_data)
            db.session.add(new_settings)
            db.session.commit()
        except Exception as e:
            return Response(json.dumps({"errors": e.args}), mimetype="application/json", status=500)

        return Response(json.dumps({'id': new_settings.id}), mimetype="application/json", status=200)


class GlobalSettingApi(Resource):
    def get(self, setting_id):
        """
        Get county specific global settings
        :param setting_id: The id of global settings
        """

        settings = db.session.query(GlobalSetting).filter_by(id=setting_id).one()
        settings_dump = json.dumps(GlobalSettingSchema().dump(settings))

        return Response(settings_dump, mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def put(self, setting_id):
        """
        Update county specific global settings
        :param setting_id: The id of global settings
        """
        json_data = request.get_json()
        json_data['id'] = setting_id
        settings = GlobalSettingSchema().load(json_data)

        db.session.add(settings)
        db.session.commit()

        return Response(json.dumps({'id': settings.id}), mimetype="application/json", status=200)
