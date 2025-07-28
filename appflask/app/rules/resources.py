from datetime import datetime

import simplejson as json
from flask import request, Response, jsonify
from flask_restful import Resource
from sqlalchemy import asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import HTTPException

from app import db, photos
from app.database.models import Property, PropertyPhoto
from app.database.models.property import PropertyPhotoSchema
from app.database.models.user import Permission
from app.routing.decorators import permission_required, Domain
from app.routing.services import PropertyService, PhotoService
from app.rules.adjustments import ALL_ADJUSTMENTS
from app.rules.models import PropertiesRules, RuleSetSchema, SelectionRules, SelectionRuleSchema, InventoryRules, \
    InventoryRuleSchema, AdjustmentSchema
from app.rules.obsolescence import ALL_OBSOLESCENCE
from app.settings.models import AssessmentDate


class RuleSetsApi(Resource):
    def get(self, assessment_date_id=None):
        """
        Get all RuleSets by optional query parameters.
            * county - filter by county name
            * town  - filter by town
            * year - filter by year
        """

        request_domain = request.headers['Host']
        if assessment_date_id is None:

            county = request.args.get('county')
            town = request.args.get('town')
            year = request.args.get('year')

            filters = {}
            if county:
                assert county in Domain.get_allowed_counties(domain=request_domain)
                filters['county'] = county
            if town:
                filters['town'] = town
            if year:
                filters['year'] = year

            query = PropertiesRules.query.filter_by(**filters)
            query = query.filter(PropertiesRules.county.in_(Domain.get_allowed_counties(domain=request_domain)))
            rule_sets = query.all()
        else:
            assessment_date = AssessmentDate.query.get(assessment_date_id)
            year = assessment_date.tax_year
            county = assessment_date.county

            assert county in Domain.get_allowed_counties(domain=request_domain)
            rule_set = PropertiesRules.load_rules(county=county, year=year)
            rule_sets = [rule_set]

        return jsonify(RuleSetSchema(many=True).dump(rule_sets))

    @permission_required(Permission.EDIT)
    def post(self):
        """
        Create a new RuleSet.
        """

        data = request.get_json()
        county = data.get('county', None)
        town = data.get('town', None)
        village = data.get('village', None)
        year = data.get('year', None)

        try:
            rule = db.session.query(PropertiesRules).filter(
                PropertiesRules.county == county,
                PropertiesRules.town == town,
                PropertiesRules.village == village,
                PropertiesRules.year == year,
            ).first()
            if rule:
                return jsonify(error='The Rule Set already exist')

            # get county rule of the last available year
            rule = db.session.query(PropertiesRules).filter(
                PropertiesRules.county == county
            ).order_by(PropertiesRules.year.desc()).first()

            # no any rule for the 'county', use global rules to pre fill
            if not rule:
                rule = PropertiesRules.load_rules()

            new_rule = RuleSetSchema().load(data)
            # pre fill from existed
            for key, value in rule.__dict__.items():
                if not key.startswith('_') and not callable(getattr(rule, key)) and key not in (
                        'rule_name', 'county', 'year', 'town', 'village', 'id', 'last_updated', 'parent'
                ):
                    if key == 'parent_id':
                        setattr(new_rule, key, rule.id)
                    else:
                        setattr(new_rule, key, value)

            db.session.add(new_rule)
            db.session.commit()
            return jsonify(RuleSetSchema().dump(new_rule))
        except IntegrityError:
            db.session.rollback()
            return jsonify(error='The Rule Set already exist')


class RuleSetApi(Resource):
    def get(self, rule_set_id):
        """
        Get specific RuleSet.
        :param rule_set_id: The RuleSet id
        """
        try:
            rule_set = PropertiesRules.query.filter_by(id=rule_set_id).first_or_404()
            dump = json.dumps(RuleSetSchema().dump(rule_set))
            return Response(dump, mimetype="application/json", status=200)
        except HTTPException:
            return Response(
                response=json.dumps({"Error": "Rule set with id={} was not found".format(rule_set_id)}),
                mimetype="application/json",
                status=404
            )

    @permission_required(Permission.EDIT)
    def put(self, rule_set_id):
        """
        Update specific RuleSet.
        :param rule_set_id: The id of RuleSet to modify
        """
        json_data = request.get_json()
        json_data['id'] = rule_set_id

        # do not allow edit year in a rule_set
        rule_set = RuleSetSchema().load(json_data, session=db.session)
        rule_set.last_updated = datetime.now()

        db.session.add(rule_set)
        db.session.commit()
        return jsonify(RuleSetSchema().dump(rule_set))

    @permission_required(Permission.EDIT)
    def delete(self, rule_set_id):
        """
        Delete specific RuleSet.
        :param rule_set_id: The id of RuleSet to delete
        """

        obj = PropertiesRules.query.filter_by(id=rule_set_id).first_or_404()
        db.session.delete(obj)
        db.session.commit()
        return jsonify({'status': True})


class InventoryRulesApi(Resource):
    def get(self, rule_set_id=None):
        """
        Get general collection of InventoryRules or sub-collection of InventoryRules by RuleSet id
        :param rule_set_id: The RuleSet id
        """
        # get general collection of InventoryRules
        if rule_set_id is None:
            inventory_rules = InventoryRules.query.order_by(asc(InventoryRules.price_start)).all()

        # get sub-collection of InventoryRules by RuleSet id
        else:
            inventory_rules = InventoryRules.query.filter_by(
                parent_id=rule_set_id
            ).order_by(asc(InventoryRules.price_start)).all()

        dump = json.dumps(InventoryRuleSchema(many=True).dump(inventory_rules))
        return Response(dump, mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def post(self):
        """
        Create new InventoryRule
        """
        json_data = request.get_json()
        new_inventory_rule = InventoryRuleSchema().load(json_data, session=db.session)
        db.session.add(new_inventory_rule)
        db.session.commit()

        return Response(json.dumps({'id': new_inventory_rule.id}), mimetype="application/json", status=200)


class InventoryRuleApi(Resource):
    def get(self, rule_id):
        """
        Get specific InventoryRule
        :param rule_id: The InventoryRule id
        """
        inventory_rule = InventoryRules.query.filter(InventoryRules.id == rule_id).first_or_404()
        dump = json.dumps(InventoryRuleSchema(many=False).dump(inventory_rule))

        return Response(dump, mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def put(self, rule_id):
        """
        Update specific InventoryRule
        :param rule_id:
        """
        json_data = request.get_json()
        json_data['id'] = rule_id
        inventory_rule = InventoryRuleSchema(many=False).load(json_data, session=db.session)

        db.session.add(inventory_rule)
        db.session.commit()

        return Response(json.dumps({'id': inventory_rule.id}), mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def delete(self, rule_id):
        """
        Delete specific InventoryRule
        :param rule_id:
        """
        inventory_rule = InventoryRules.query.filter(InventoryRules.id == rule_id).first_or_404()
        db.session.delete(inventory_rule)
        db.session.commit()

        return Response(json.dumps({'status': True}), mimetype="application/json", status=200)


class SelectionRulesApi(Resource):

    def get(self, rule_set_id=None):
        """
        Get general collection of SelectionRules or sub-collection of SelectionRules by RuleSet id
        """

        # get general collection of SelectionRules
        if rule_set_id is None:
            selection_rules = SelectionRules.query.all()

        # get sub-collection of SelectionRules by RuleSet id
        else:
            selection_rules = SelectionRules.query.filter_by(parent_id=rule_set_id).all()

        dump = json.dumps(SelectionRuleSchema(many=True).dump(selection_rules))
        return Response(dump, mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def post(self):
        """
        Create new SelectionRule
        """
        json_data = request.get_json()
        new_selection_rule = SelectionRuleSchema().load(json_data, session=db.session)

        db.session.add(new_selection_rule)
        db.session.commit()

        return Response(json.dumps({'id': new_selection_rule.id}), mimetype="application/json", status=200)


class SelectionRuleApi(Resource):
    def get(self, rule_id):
        """
        Get specific SelectionRule
        :param rule_id: The SelectionRule id
        """

        # get specific SelectionRule
        selection_rule = SelectionRules.query.filter_by(id=rule_id).first_or_404()
        dump = json.dumps(SelectionRuleSchema(many=False).dump(selection_rule))

        return Response(dump, mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def put(self, rule_id):
        """
        Update specific SelectionRule
        :param rule_id: The SelectionRule id
        """
        json_data = request.get_json()
        json_data['id'] = rule_id

        selection_rule = SelectionRuleSchema(many=False).load(json_data, session=db.session)
        db.session.add(selection_rule)
        db.session.commit()

        return Response(json.dumps({'id': selection_rule.id}), mimetype="application/json", status=200)

    @permission_required(Permission.EDIT)
    def delete(self, rule_id):
        """
        Delete specific SelectionRule
        :param rule_id:
        """
        selection_rule = SelectionRules.query.filter_by(id=rule_id).first_or_404()
        db.session.delete(selection_rule)
        db.session.commit()

        return Response(json.dumps({'status': True}), mimetype="application/json", status=200)


class AdjustmentsApi(Resource):
    def get(self):
        """
        Get all adjustments
        """
        # prepare adjustments to the response
        # push adjustment key to response object
        adjustments = []
        for key in ALL_ADJUSTMENTS.keys():
            adjustment = ALL_ADJUSTMENTS[key]
            adjustment['key'] = key
            adjustments.append(adjustment)

        dump = json.dumps(AdjustmentSchema(many=True).dump(adjustments))
        return Response(dump, mimetype="application/json", status=200)


class ObsolescenceApi(Resource):
    def get(self):
        """
        Get all obsolescence by county
        """
        county = request.args.get('county')
        if county:
            obsolescence = ALL_OBSOLESCENCE.get(county, {})
        else:
            obsolescence = {}
            for county in ALL_OBSOLESCENCE.keys():
                obsolescence.update(ALL_OBSOLESCENCE.get(county, {}))
        return Response(json.dumps(obsolescence), mimetype="application/json", status=200)


class BestPropertiesPhotosApi(Resource):
    def get(self):
        best_photos = {}
        json_data = request.get_json()
        properties = json_data['properties']
        for prop_id in properties:
            try:
                best_photo = PropertyPhoto.query.filter_by(property_id=prop_id,
                                                           is_best=True).one()
                prop = Property.query.filter_by(id=prop_id).one()
                best_photos[prop_id] = photos.url(f'{prop.county}/photos/{best_photo.name}')
            except NoResultFound:
                resp = jsonify({'message':
                                f'No best photo set for property with id {prop_id}'})
                resp.status_code = 400
                return resp

        resp = jsonify(best_photos)
        resp.status_code = 400
        return resp


class BestPropertyPhotoApi(Resource):
    def get(self, property_id):
        prop = Property.query.get(property_id)
        if not prop:
            resp = jsonify({'message': f'No property found with id {property_id}'})
            resp.status_code = 400
            return resp
        try:
            best_photo = PropertyPhoto.query.filter_by(property_id=prop.id,
                                                       is_best=True).one()
        except NoResultFound:
            resp = jsonify({'message':
                            f'No best photo set for property with id {property_id}'})
            resp.status_code = 400
            return resp

        resp = jsonify({
            'id': best_photo.id,
            'url': photos.url(f'{prop.county}/photos/{best_photo.name}')
        })
        resp.status_code = 200
        return resp

    @permission_required(Permission.EDIT)
    def patch(self, property_id):
        prop = Property.query.get(property_id)
        if not prop:
            resp = jsonify({'message': f'No property found with id {property_id}'})
            resp.status_code = 400
            return resp

        json_data = request.get_json()
        photo_id = json_data['id']

        q = PropertyPhoto.query.filter_by(id=photo_id, property_id=prop.id)
        if not q.first():
            resp = jsonify({'message': f'Photo not related to property with id {property_id}'})
            resp.status_code = 400
            return resp

        PropertyPhoto.query.filter_by(property_id=prop.id).update({
            'is_best': False
        })

        q.update({
            'is_best': True
        })

        db.session.commit()

        resp = jsonify({'message': 'success'})
        resp.status_code = 400
        return resp


class PhotosApi(Resource):

    @classmethod
    def not_found(cls, message):
        return Response(
            response=json.dumps({'message': message}),
            mimetype="application/json",
            status=400
        )

    def _get_folder_path(self, prop):
        return photos.config.destination / prop.county / 'photos'

    def _make_photos(self, prop):

        # assign photos ranks
        all_photos = PhotoService.get_rank_photos(prop.id)

        # assign photos url
        for photo in all_photos:
            photo.url = PhotoService.make_photo_url(prop, photo)

        return all_photos

    def get(self, property_id=None):
        """
        Get all property photos sub-collection or all best photos
        """
        # get all property photos sub-collection
        if property_id:

            p = PropertyService.get_property(property_id)
            if not p:
                return self.not_found(message=f'No property found with id {property_id}')

            collection = self._make_photos(p)

        # get all best photos for the requested property ids
        else:

            json_data = request.get_json()
            properties = json_data['properties']
            collection = []
            try:
                for property_id in properties:
                    photo = PhotoService.get_best_photo(property_id)
                    prop = PropertyService.get_property(property_id)
                    photo.url = PhotoService.make_photo_url(prop, photo)

                    collection.append(photo)
            except NoResultFound:
                return self.not_found(message=f'No best photo set for property with id {property_id}')

        return Response(
            response=json.dumps(PropertyPhotoSchema().dump(collection, many=True)),
            mimetype="application/json",
            status=200
        )

    @permission_required(Permission.EDIT)
    def post(self, property_id):
        """
        Upload property photo
        """

        # check supplied property id
        p = PropertyService.get_property(property_id)
        if not p:
            return self.not_found(message=f'No property found with id {property_id}')

        if 'property_photo' not in request.files:
            return self.not_found(message='No file part in the request')

        file = request.files['property_photo']
        is_best = request.args.get('is_best', False, type=bool)

        if file.filename == '':
            return self.not_found(message='No file selected for uploading')

        # create photo name
        photo_name = PhotoService.get_photo_name(file)

        # store photo to database
        try:
            new_photo = PropertyPhoto(property_id=property_id, name=photo_name)
            new_photo.url = PhotoService.make_photo_url(p, new_photo)
            new_photo.is_best = is_best
            db.session.add(new_photo)
            db.session.commit()
        except IntegrityError:
            return Response(
                response=json.dumps({'message': 'Photo has been uploaded before'}),
                mimetype="application/json",
                status=400
            )

        # store photo on server
        photos.save(file, name=photo_name, folder=self._get_folder_path(p))

        return Response(json.dumps(PropertyPhotoSchema().dump(new_photo)), mimetype="application/json", status=201)


class PhotoApi(Resource):
    def get(self, property_id, photo_id=None):
        """
        Get any or best property photo
        """

        prop = PropertyService.get_property(property_id)
        if not prop:
            return PhotosApi.not_found(message=f'No property found with id {property_id}')
        try:
            # get any property photo by id
            if photo_id:
                photo = PropertyPhoto.query.filter_by(id=photo_id, property_id=property_id).first_or_404()

            # get best property photo
            else:
                photo = PhotoService.get_best_photo(property_id=property_id)
            photo.url = PhotoService.make_photo_url(prop, photo)
        except NoResultFound:
            return PhotosApi.not_found(message=f'No best photo set for property with id {property_id}')

        return Response(
            response=json.dumps(PropertyPhotoSchema().dump(photo, many=False)),
            mimetype="application/json",
            status=200
        )

    @permission_required(Permission.EDIT)
    def put(self, property_id, photo_id):
        """
        Update property photo
        """
        json_data = request.get_json()
        json_data['id'] = photo_id
        json_data['property_id'] = property_id

        PropertyPhoto.query.filter_by(property_id=property_id, is_best=True).update({'is_best': False})
        updated_photo = PropertyPhotoSchema().load(json_data)
        updated_photo.created_at = datetime.now()

        db.session.add(updated_photo)
        db.session.commit()

        prop = PropertyService.get_property(property_id)
        updated_photo.url = PhotoService.make_photo_url(prop, updated_photo)

        return Response(
            response=json.dumps(PropertyPhotoSchema().dump(updated_photo)),
            mimetype="application/json",
            status=200
        )

    @permission_required(Permission.EDIT)
    def delete(self, property_id, photo_id):
        """
        Delete property photo
        """
        obj = PropertyPhoto.query.filter_by(id=photo_id, property_id=property_id).first_or_404()
        db.session.delete(obj)
        db.session.commit()

        return Response(json.dumps({'status': True}), mimetype="application/json", status=200)
