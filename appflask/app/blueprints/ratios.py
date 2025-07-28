from flask import Blueprint, render_template
from flask_security import login_required

bp = Blueprint('ratios', __name__, url_prefix='/ratios')


@bp.route('/')
@login_required
def index():
    return render_template('ratios.html')
