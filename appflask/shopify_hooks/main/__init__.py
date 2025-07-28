from flask import Blueprint

main = Blueprint('webhooks_main', __name__)

from . import views  # NOQA
