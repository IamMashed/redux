from flask import Blueprint
from flask_restful import Api
from .api import PublicApiResourceManager
from flask_cors import CORS

bp_api = Blueprint('api', __name__)
CORS(bp_api)

api = Api(bp_api, prefix='/api')
api_manager = PublicApiResourceManager(api)
api_manager.init_resources()
