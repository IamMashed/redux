from flask import Flask
from flask_mail import Mail

import config  # noqa
from app import db

mail = Mail()


def create_app():
    app = Flask(__name__)

    app.config.from_object('config')

    db.init_app(app)
    mail.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import bp_api as api_blueprint
    app.register_blueprint(api_blueprint)

    # do not log when mail is sent
    app.extensions['mail'].debug = 0

    return app
