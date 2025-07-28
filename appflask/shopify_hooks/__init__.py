from flask import Flask

import config  # noqa
from app import db


def create_app():
    app = Flask(__name__)

    app.config.from_object('config')

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #  from .api import bp_api as api_blueprint
    #  app.register_blueprint(api_blueprint)

    return app
