from collections import OrderedDict

from flask import Response, request, redirect
from flask_restful import Resource
from flask_restful.representations import json

from app.utils.constants import (DISTANCE_UNITS, BASEMENT_TYPE_MAP, PATIO_TYPE_MAP, PAVING_TYPE_MAP,
                                 HEAT_TYPE_MAP, PORCH_TYPE_MAP, PROPERTY_STYLE_MAP,
                                 PROPERTY_LAND_TAGS, PROPERTY_WATER_CATEGORY, WHITELISTED_PROPERTY_CLASS_CODES)
from gcmaportal.main.views import REDUX_URL

ALL_CONSTANTS = {
    'distance_units': DISTANCE_UNITS,
    'basement_type_map': BASEMENT_TYPE_MAP,
    'patio_type_map': PATIO_TYPE_MAP,
    'paving_type_map': PAVING_TYPE_MAP,
    'heat_type_map': HEAT_TYPE_MAP,
    'porch_type_map': PORCH_TYPE_MAP,
    'property_style_map': PROPERTY_STYLE_MAP,
    'property_classes_map': WHITELISTED_PROPERTY_CLASS_CODES,
    'land_tag_map': PROPERTY_LAND_TAGS,
    'water_category_map': PROPERTY_WATER_CATEGORY
}


class ConstantsApi(Resource):

    def get(self):
        """
        Get all project constants or constants by county name.
            params: county: The county
        """
        county_name = request.args.get('county', None)

        # get all county constants
        if county_name:
            county_constants = {}
            for k, v in ALL_CONSTANTS.items():
                county_constants[k] = v.get(county_name, OrderedDict())
            return Response(json.dumps(county_constants, sort_keys=True), mimetype="application/json", status=200)

        return Response(json.dumps(ALL_CONSTANTS, sort_keys=True), mimetype="application/json", status=200)


class ConfirmEmailApi(Resource):
    def get(self, token):
        # TODO: get properly redirect url
        return redirect(REDUX_URL)
