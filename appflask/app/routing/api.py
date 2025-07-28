from flask import Blueprint, g, jsonify, request
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from flask_security import current_user
from flask_security.utils import verify_password as security_verify_password

from app.database.models import User
from app.routing import ApiResourceManager
from app.routing.errors import unauthorized, ValidationError, bad_request, forbidden
from config import FLASK_CORS

bp = Blueprint('api', __name__)

# Allow CORS request if is allowed by env
if FLASK_CORS == 'True':
    CORS(bp, supports_credentials=True, automatic_options=True)

api = Api(bp, prefix='/api')
api_manager = ApiResourceManager(api)
api_manager.init_resources()

auth = HTTPBasicAuth()


@bp.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])


@auth.verify_password
def verify_password(email_or_token, password):
    if not current_user.is_anonymous:
        g.current_user = current_user
        return True
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token.lower()).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return security_verify_password(password, user.password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@bp.before_request
@auth.login_required
def before_request():
    if FLASK_CORS == 'True' and request.method == 'OPTIONS':
        return
    if g.current_user.is_anonymous:
        return forbidden('Unconfirmed account')


@bp.route('/tokens/', methods=['POST'])
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})
