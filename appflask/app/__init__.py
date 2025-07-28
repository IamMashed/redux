from flask_login import LoginManager
from flask_mail import Mail
from flask_uploads import UploadSet, IMAGES, configure_uploads
from redis import Redis
import rq
from flask import Flask, request
from flask_security import Security, SQLAlchemyUserDatastore
from flask_bootstrap import Bootstrap
from flask_babelex import Babel
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_marshmallow import Marshmallow

import config

from app.database import db
from app.database import models
from app.database.models.property import TOWNS
from app.rules.adjustments import ALL_ADJUSTMENTS
from app.rules.obsolescence import ALL_OBSOLESCENCE
from app.security import ExtendedLoginForm
from app.routing import Routing
from app.utils.constants import BASEMENT_TYPE_MAP, get_rule_for
from app.routing.decorators import Domain

bootstrap = Bootstrap()
babel = Babel()
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security()
routing = Routing()
csrf = CSRFProtect()
ma = Marshmallow()
mail = Mail()
migrate = Migrate(compare_type=True)
photos = UploadSet('photos', IMAGES)

login_manager = LoginManager()
login_manager.login_view = 'security.login'
login_manager.anonymous_user = models.AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)

    app.jinja_env.globals['TOWNS'] = TOWNS
    app.jinja_env.globals['ALL_OBSOLESCENCE'] = ALL_OBSOLESCENCE
    app.jinja_env.globals['ALL_ADJUSTMENTS'] = ALL_ADJUSTMENTS
    app.jinja_env.globals['BASEMENT_TYPE_MAP'] = BASEMENT_TYPE_MAP
    app.jinja_env.globals['get_rule_for'] = get_rule_for
    app.jinja_env.globals['DOMAIN'] = Domain

    app.config.from_object('config')

    db.init_app(app)
    migrate.init_app(app, db)
    security.init_app(app, user_datastore, login_form=ExtendedLoginForm)
    ma.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    routing.init_app(app)
    login_manager.init_app(app)

    from .blueprints.admin import admin
    app.register_blueprint(admin)

    from .blueprints.masscma import bp as masscma
    app.register_blueprint(masscma)

    from .blueprints.bounce import bp as bounces
    app.register_blueprint(bounces)

    from .blueprints.singlecma import bp as singlecma
    app.register_blueprint(singlecma)

    from .blueprints.rulesets import ruleset
    app.register_blueprint(ruleset)

    from .blueprints.commands import bp as commands
    app.register_blueprint(commands)

    from .blueprints.case_management import bp as case_management
    app.register_blueprint(case_management)

    from .blueprints.match_owners import bp as match_owners
    app.register_blueprint(match_owners)

    from .blueprints.obsolescence import bp as obsolescence
    app.register_blueprint(obsolescence)

    from .blueprints.ratios import bp as ratios
    app.register_blueprint(ratios)

    from .routing.api import bp as bp_api
    app.register_blueprint(bp_api)

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('globalcma-tasks', connection=app.redis)

    configure_uploads(app, photos)

    app.extensions['mail'].debug = 0

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(config.LANGUAGES)
