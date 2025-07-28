import click

from flask import Blueprint, render_template
from flask_security import login_required
from sqlalchemy.sql.expression import func

from app import db
from app.database.models import Property
from app.routing.services import PropertyService
from app.singlecma.services import SingleCMAService
from app.utils.comp_utils import get_whitelisted

bp = Blueprint('singlecma', __name__, url_prefix='/cma')


@bp.route('/')
@login_required
def index():
    random_prop = db.session.query(Property).filter(Property.assessments, Property.county == 'nassau').order_by(
        func.random()).first()
    print(random_prop.__dict__)
    return render_template('select_cma.html',
                           random_property=random_prop)


@bp.cli.command('find_subjects_with_comps')
@click.argument('county')
@click.argument('amount', type=click.INT)
@click.argument('min_comps_count', type=click.INT, default=5)
def find_subjects_with_comps(county, amount, min_comps_count):
    """
    Get a 'amount' of subject id's that cma produce 'min_comps_count' comparables
    :param county: The county
    :param amount
    """
    properties = PropertyService.search_properties(args={'county': county, 'limit': 1000})
    properties = get_whitelisted(properties)

    # run cma and if there are comps add to result list
    ids = []
    for p in properties:
        subject = PropertyService.get_property(p.id)

        if subject is None:
            continue

        # the property assessment
        assessment = PropertyService.get_property_assessment(subject.id)

        if not assessment:
            continue

        if subject.geo is None:
            continue

        # compute single cma
        cma_results = SingleCMAService.compute_single_cma(subject=subject, assessment=assessment)
        if len(cma_results.get('all_comps')) > min_comps_count:
            ids.append(p.id)

        if len(ids) > amount:
            break

    print(f"The list of subject's id's for county={county} that cma produce at least {amount} comps:")
    print(ids)
