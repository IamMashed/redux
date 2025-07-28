from collections import namedtuple
from concurrent.futures import as_completed, ProcessPoolExecutor

import click
from flask import Blueprint
from sqlalchemy import func

from app import db
from app.database.models import Owner

from fuzzywuzzy import fuzz
from itertools import combinations

from config import MAX_WORKER_COUNT

bp = Blueprint('match', __name__)


def compute_ratio(first, second):
    ratio1 = fuzz.token_set_ratio(first.first_name, second.first_name)
    ratio2 = fuzz.token_set_ratio(first.first_name, second.second_name)
    ratio3 = fuzz.token_set_ratio(first.second_name, second.first_name)
    ratio4 = fuzz.token_set_ratio(first.second_name, second.second_name)
    return max(ratio1, ratio2, ratio3, ratio4)


def update_matched(first, second):
    first = Owner.query.get(first.owner_id)
    if not first.matching:
        first.matching = True
    second = Owner.query.get(second.owner_id)
    if not second.matching:
        second.matching = True
    db.session.commit()


def update_unmatched(first, second):
    first = Owner.query.get(first.owner_id)
    if first.matching is None:
        first.matching = False
    second = Owner.query.get(second.owner_id)
    if second.matching is None:
        second.matching = False
    db.session.commit()


def match(unmatched_list):
    for c in combinations(unmatched_list, 2):
        ratio = compute_ratio(*c)
        if ratio > 90:
            update_matched(*c)
        else:
            update_unmatched(*c)
    return


FullName = namedtuple('Full_name', 'source first_name second_name owner_id')


def match_attempt(record):
    from manage import app
    with app.app_context():
        yet_unmatched = Owner.query.filter_by(property_id=record[0]).all()
        unmatched = list()
        for r in yet_unmatched:
            first = ' '.join([r.first_name or '', r.last_name or '']).strip()
            second = ' '.join([r.second_owner_first_name or '',
                               r.second_owner_last_name or '']).strip()
            unmatched.append(FullName(r.data_source, first, second, r.id))
        match(unmatched)


@bp.cli.command('owners')
def owners():
    duplicates = db.session.query(Owner.property_id).having(func.count(Owner.property_id) > 1).group_by(
        Owner.property_id).all()
    with ProcessPoolExecutor(MAX_WORKER_COUNT) as executor:
        futures = (executor.submit(match_attempt, record) for record in duplicates)
        with click.progressbar(length=len(duplicates), label='matching names') as bar:
            for _ in as_completed(futures):
                bar.update(1)
    return None
