import io
import gc
import csv
import sys
import traceback
from collections import namedtuple
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

import click
from datetime import date
from flask import Blueprint, render_template, request, make_response, flash, jsonify, redirect, current_app, url_for
from flask_login import current_user
from flask_security import login_required
from sqlalchemy import and_, desc, asc, or_
from sqlalchemy.orm import aliased
from tqdm import tqdm

from app.blueprints.forms.mass_cma import MassCmaRunForm, MassCmaFilterForm, MassCmaSelectForm
from app.database import db
from app.database.models import CmaResult, Owner, CmaTask, Assessment, Sale
from app.database.models.property import Property, TOWNS
from app.controller.properties_controller import SingleCmaController
from app.database.models.user import Notification, UserMassCmaFilter, Permission
from app.routing.decorators import permission_required
from app.routing.services import PropertyService
from app.rules.controllers import RulesController
from app.rules.exceptions import NotEnoughCompsException, SubjectLacksDataException
from app.rules.models import PropertiesRules
from app.settings.models import AssessmentDate, Ratio, TimeAdjustmentValue
from app.utils.constants import get_all_towns, get_town_code, NASSAU_VILLAGES, get_nassau_villages, get_townships
from config import MAX_WORKER_COUNT, DATA_IMPORT

bp = Blueprint('masscma', __name__, url_prefix='/masscma')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = MassCmaRunForm()
    form.county.choices = [(town, town.capitalize()) for town in TOWNS.keys()]
    form.assessment.choices = AssessmentDate.select_field_choices()
    nassau_villages = get_nassau_villages()
    suffolk_towns = get_townships(TOWNS, 'suffolk')
    form.village.choices = nassau_villages + suffolk_towns

    cma_tasks = CmaTask.query.filter(CmaTask.complete.is_(True)).order_by(CmaTask.task_ts.desc()).limit(10).all()
    task_id = cma_tasks[0].id if cma_tasks else None
    select_form = MassCmaSelectForm()
    select_form.computed_mass_cma.choices = [(foo.id, f"{foo.county_name.upper()} "
                                                      f"{foo.task_ts.strftime('%d %b %Y %H:%M')}")
                                             for foo in cma_tasks]

    filter_form = MassCmaFilterForm()
    filter_form.county.choices = [(town, town.capitalize()) for town in TOWNS.keys()]
    filter_form.county.choices.insert(0, ('', 'Select County:'))
    filter_form.town.choices = [(town, town) for town in get_all_towns(TOWNS)]
    filter_form.town.choices.insert(0, ('', 'Select Township:'))
    filter_form.village.choices = NASSAU_VILLAGES

    if select_form.data and select_form.validate_on_submit():
        task_id = select_form.computed_mass_cma.data

    if form.start.data and form.validate_on_submit() and current_user.can(
            Permission.MASS_CMA):
        if CmaTask.get_task_in_progress():
            flash('Mass CMA task is currently in progress')
        else:
            current_user.launch_task(name='mass_cma',
                                     description=f'Mass CMA for {form.county.data}',
                                     county=form.county.data,
                                     village=form.village.data,
                                     assessment_date_id=form.assessment.data,
                                     assessment_stage=form.assessment_stage.data,
                                     sale_dates_from=form.sale_dates_from.data,
                                     sale_dates_to=form.sale_dates_to.data)

    if form.stop.data:
        current_task = CmaTask.get_task_in_progress()
        if current_task:
            current_app.task_queue.delete(delete_jobs=True)
            current_task.complete = True
            db.session.commit()

    page = request.args.get('page', 1, type=int)
    if not task_id:
        return render_template('mass_cma.html', items=[], pagination=None, form=form, select_form=select_form,
                               filter_form=filter_form, sort_info=dict(
                column_name='saving',
                direction='asc',
            ))
    selected_cma_task = CmaTask.query.get(task_id)

    # selecting the latest sale of property
    last_sale = aliased(Sale, name='last')
    last_id = (
        db.session.query(last_sale.id)
        .filter(last_sale.property_id == Property.id)
        .order_by(last_sale.date.desc())
        .limit(1)
        .correlate(Property)
        .as_scalar()
    )

    q = db.session.query(CmaResult,
                         Property,
                         CmaTask,
                         Assessment,
                         Sale).filter(
        CmaResult.task_id == task_id,
        or_(CmaResult.computed_cma.isnot(None), CmaResult.subject_sale.isnot(None))).join(
        Property,
        Property.id == CmaResult.property_id).join(
        CmaTask, CmaTask.id == CmaResult.task_id).join(
        Assessment, and_(
            Assessment.property_id == Property.id,
            Assessment.assessment_id == CmaTask.assessment_date_id)
    ).outerjoin(Sale, Sale.id == last_id)

    assessment_ratio = Ratio.get_ratio(selected_cma_task.assessment_date.valuation_date.year,
                                       selected_cma_task.county_name)

    # filtering
    if current_user.mass_cma_filter and request.method == 'GET':
        q = current_user.apply_mass_cma_filter(q, assessment_ratio, form=filter_form)

    if filter_form.validate_on_submit() and filter_form.apply.data:
        page = 1
        user_mass_cma_filter = current_user.mass_cma_filter or UserMassCmaFilter()

        county = filter_form.county.data
        user_mass_cma_filter.county = county or None
        if county:
            q = q.filter(Property.county == county)

        town = filter_form.town.data
        town_code = get_town_code(TOWNS, county, town)
        user_mass_cma_filter.town = town_code
        if town:
            q = q.filter(Property.town == town_code)

        vill = filter_form.village.data
        user_mass_cma_filter.village = vill
        if vill:
            if vill == 'No Village':
                q = q.filter(Property.village.is_(None))

            elif vill == 'None':
                user_mass_cma_filter.village = None
            else:
                q = q.filter(Property.village == vill)

        section = filter_form.section.data
        user_mass_cma_filter.section = section or None
        if section:
            q = q.filter(Property.section == section)

        block = filter_form.block.data
        user_mass_cma_filter.block = block or None
        if block:
            q = q.filter(Property.block == block)

        lot = filter_form.lot.data
        user_mass_cma_filter.lot = lot or None
        if lot:
            q = q.filter(Property.lot == lot)

        street = filter_form.street.data
        user_mass_cma_filter.street = street or None
        if street:
            q = q.filter(Property.street.ilike(street))

        number = filter_form.number.data
        user_mass_cma_filter.number = number or None
        if number:
            q = q.filter(Property.number == number)

        school = filter_form.school_district.data
        user_mass_cma_filter.school_district = school or None
        if filter_form.school_district.data:
            q = q.filter(Property.school_district == school)

        saving_min = filter_form.saving_min.data
        user_mass_cma_filter.saving_min = saving_min or None
        if filter_form.saving_min.data:
            q = q.filter((Assessment.assessment_value - CmaResult.computed_cma) >=
                         int(saving_min))

        saving_max = filter_form.saving_max.data
        user_mass_cma_filter.saving_max = saving_max or None
        if filter_form.saving_max.data:
            q = q.filter((Assessment.assessment_value - CmaResult.computed_cma) <=
                         int(saving_max))

        subject_sale_min = filter_form.subject_sale_min.data
        user_mass_cma_filter.subject_sale_min = subject_sale_min or None
        if filter_form.subject_sale_min.data:
            q = q.filter(CmaResult.subject_sale >=
                         int(subject_sale_min))

        subject_sale_max = filter_form.subject_sale_max.data
        user_mass_cma_filter.subject_sale_max = subject_sale_max or None
        if filter_form.subject_sale_max.data:
            q = q.filter(CmaResult.subject_sale <=
                         int(saving_max))

        min_ = filter_form.market_value_min.data
        user_mass_cma_filter.market_value_min = min_ or None
        if filter_form.market_value_min.data:
            q = q.filter((Assessment.value / assessment_ratio) >=
                         int(min_))

        max_ = filter_form.market_value_max.data
        user_mass_cma_filter.market_value_max = max_ or None
        if filter_form.market_value_max.data:
            q = q.filter((Assessment.value / assessment_ratio) <=
                         int(max_))

        user_mass_cma_filter.user_id = current_user.id
        db.session.add(user_mass_cma_filter)
        db.session.commit()

    if filter_form.clear.data:
        if current_user.mass_cma_filter:
            db.session.delete(current_user.mass_cma_filter)
            db.session.commit()
        return redirect(request.referrer)

    # ordering
    cn = request.args.get('column_name')
    d = request.args.get('direction')
    p = request.args.get('page')
    if cn and not p:
        d = 'asc' if d == 'desc' else 'desc'

    if cn and q.count():
        order_direction = asc if d == 'asc' else desc
        if cn == 'saving':
            q = q.order_by(order_direction(Assessment.assessment_value - CmaResult.computed_cma))
            pass
        elif cn == 'apn':
            q = q.order_by(order_direction(Property.apn))
        # TODO: implement the previous client
        elif cn == 'previous_client':
            pass
        elif cn == 'county_tentative_assessment':
            q = q.order_by(order_direction(Assessment.value))
        elif cn == 'gd_avg_1_4':
            q = q.order_by(order_direction(CmaResult.computed_cma_good_small))

        elif cn == 'gd_avg_1_8':
            q = q.order_by(order_direction(CmaResult.computed_cma_good_medium))

        elif cn == 'gd_avg_1_12':
            q = q.order_by(order_direction(CmaResult.computed_cma_good_high))

        elif cn == 'all_avg_1_4':
            q = q.order_by(order_direction(CmaResult.computed_cma))

        elif cn == 'all_avg_1_8':
            q = q.order_by(order_direction(CmaResult.computed_cma_medium))

        elif cn == 'all_avg_1_12':
            q = q.order_by(order_direction(CmaResult.computed_cma_high))

        elif cn == 'total_good_comps':
            q = q.order_by(order_direction(CmaResult.total_good_comps))

        elif cn == 'total_comps':
            q = q.order_by(order_direction(CmaResult.total_all_comps))

        elif cn == 'subject_sale':
            q = q.order_by(order_direction(CmaResult.subject_sale))

        elif cn == 'assessed_market':
            q = q.order_by(order_direction(Assessment.value / assessment_ratio))
        elif cn == 'cma_market':
            q = q.order_by(order_direction(CmaResult.computed_cma / assessment_ratio))

        elif cn == 'sale_price':
            q = q.order_by(order_direction(Sale.price))

        elif cn == 'sale_date':
            q = q.order_by(order_direction(Sale.date))

        elif cn == 'county':
            q = q.order_by(order_direction(Property.county))
        elif cn == 'town':
            q = q.order_by(order_direction(Property.town))
        elif cn == 'street':
            q = q.order_by(order_direction(Property.street))
        elif cn == 'house_number':
            q = q.order_by(order_direction(Property.number))
        elif cn == 'school':
            q = q.order_by(order_direction(Property.school_district))

    # default sort by saving
    if not request.args:
        cn = 'saving'
        q = q.order_by(desc(Assessment.assessment_value - CmaResult.computed_cma))

    sort_info = dict(
        column_name=cn,
        direction=d,
    )
    pagination = q.paginate(page=page, per_page=30, error_out=False) if selected_cma_task else None
    return render_template('mass_cma.html',
                           assessment_ratio=assessment_ratio,
                           items=pagination.items if pagination else [],
                           pagination=pagination,
                           form=form,
                           filter_form=filter_form,
                           select_form=select_form,
                           sort_info=sort_info,
                           task_id=task_id
                           )


@bp.route('/notifications')
@login_required
@permission_required(Permission.MASS_CMA)
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])


@bp.route('/download_csv', methods=['POST'])
@login_required
def download_csv():
    """
    Export to csv the information from the mass cma page.
    Columns to include:
    Subject Address
    Legal address (FOLIO or SBL number)
    Owner's Address
    Owner first name
    Owner last name
    Second Owner First Name,
    Second Owner Last name,
    Calculated savings
    """
    with io.StringIO() as si:
        from_ = request.form.get('from')
        to_ = request.form.get('to')

        from_ = int(from_) if from_ else None
        to_ = int(to_) if to_ else None

        if to_ and from_ and to_ < from_:
            flash('To value has to be greater than From')
            return redirect(url_for('masscma.index'))

        if to_ and from_:
            to_ = to_ - from_

        task_id = request.form.get('task_id')
        latest_cma_task = CmaTask.query.get(task_id)

        if not latest_cma_task:
            flash('Task ID not found', category='error')
            return redirect(url_for('masscma.index'))

        q = db.session.query(CmaResult,
                             Property.address,
                             Property.apn,
                             Assessment.assessment_value,
                             Owner,
                             Assessment.value).filter(
            CmaResult.task_id == task_id,
            or_(CmaResult.computed_cma.isnot(None), CmaResult.subject_sale.isnot(None))).join(
            Property,
            Property.id == CmaResult.property_id).join(
            CmaTask, CmaTask.id == CmaResult.task_id).join(
            Assessment, and_(
                Assessment.property_id == Property.id,
                Assessment.assessment_id == CmaTask.assessment_date_id)).join(
            Owner,
            and_(Owner.property_id == Property.id,
                 Owner.data_source == 'assessment'))

        q = q.order_by(Property.id)

        if from_:
            q = q.offset(from_)
        if to_:
            q = q.limit(to_)

        assessment_ratio = Ratio.get_ratio(
            latest_cma_task.assessment_date.valuation_date.year,
            latest_cma_task.county_name)
        if current_user.mass_cma_filter:
            q = current_user.apply_mass_cma_filter(q, assessment_ratio)

        items = q.all()
        # output = None
        cw = csv.writer(si)
        cw.writerow(['Subject Address', 'Legal address', 'Previous Client',
                     'County Tentative Assessment',
                     'Market Value',
                     'Owner Full Name',
                     'Second Owner Full Name',
                     'Owner Address Line 1', 'Owner Address Line 2',
                     'Owner Address Line 3', 'Owner Address City',
                     'Owner Address Zip', 'Owner Address State',
                     'Savings', 'Subject Sale',
                     'Good Average 1-4',
                     'Good Average 1-8',
                     'Good Average 1-12', 'All Average 1-4', 'All Average 1-8',
                     'All Average 1-12',
                     'Total Good Comparables', 'Total All Comparables'])

        progress = tqdm(total=len(items))
        seen_properties = set()
        for item in items:
            progress.update(1)

            subject_address = item[1] or ''
            legal_address = item[2] or ''
            if legal_address in seen_properties:
                continue

            # TODO: to be revised with case management
            previous_client = 'N'
            assessment_value = item[3]
            market_value = item[5]

            owner_first_name = item.Owner.first_name or ''
            owner_last_name = item.Owner.last_name or ''
            owner_full_name = ' '.join([owner_first_name, owner_last_name])

            second_owner_first_name = item.Owner.second_owner_first_name or ''
            second_owner_last_name = item.Owner.second_owner_last_name or ''
            second_owner_full_name = ' '.join([second_owner_first_name, second_owner_last_name])

            if item.CmaResult.computed_cma:
                saving = str(int(assessment_value - item.CmaResult.computed_cma))
            else:
                saving = item.CmaResult.subject_sale or ''

            subject_sale = item.CmaResult.subject_sale_price if not item.CmaResult.computed_cma else None

            good_average_small = item.CmaResult.computed_cma_good_small or ''
            good_average_medium = item.CmaResult.computed_cma_good_medium or ''
            good_average_high = item.CmaResult.computed_cma_good_high or ''
            all_average_small = item.CmaResult.computed_cma or ''
            all_average_medium = item.CmaResult.computed_cma_medium or ''
            all_average_high = item.CmaResult.computed_cma_high or ''
            total_good_comps = item.CmaResult.total_good_comps or ''
            total_all_comps = item.CmaResult.total_all_comps

            row = [subject_address, legal_address, previous_client, assessment_value,
                   market_value,
                   owner_full_name, second_owner_full_name,
                   item.Owner.owner_address_1 or '',
                   item.Owner.owner_address_2 or '',
                   item.Owner.owner_address_3 or '',
                   item.Owner.owner_city or '',
                   item.Owner.owner_zip or '',
                   item.Owner.owner_state or '',
                   saving, subject_sale or '',
                   good_average_small,
                   good_average_medium, good_average_high, all_average_small,
                   all_average_medium,
                   all_average_high, total_good_comps, total_all_comps]
            cw.writerow(row)
            seen_properties.add(legal_address)

        # Clear out ram from sqlalchemy
        db.session.flush()
        db.session.expunge_all()
        db.session.close()

        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=mass_cma.csv"
        output.headers["Content-type"] = "text/csv"

    # Clear out RAM from internal variables including StringIO we just used
    gc.collect()

    return output


@bp.cli.command('cma_property')
@click.argument('prop_id')
def cma_property(prop_id):
    """Run Comparative Market Analysis on one property"""
    try:
        subj = db.session.query(Property).filter(Property.id == prop_id).one()
        cma = SingleCmaController(subj, mass_cma=False)
        cma.compute_cma()
        result = cma.get_all_avg_ranges()
        print(f'computed cma for property id {cma.subject_property.id} is {result}')
    except (NotEnoughCompsException, SubjectLacksDataException) as e:
        print(e)


@bp.cli.command('mass_cma_property')
def mass_cma_property():
    """Run Mass Comparative Market Analysis on three sample properties"""
    props = [
        1280797,
        1245586,
        714120,
        1001412,
        # 3016518,  # suffolk
        # 2765153,
        # 366219,
        # 2687761,
        # 2726267,
        # 274599,
        # 274857,
        # 275302,
        # 275666,
        # 276100
    ]
    assessment_date = AssessmentDate.query.get(5)

    # tax_year = assessment_date.tax_year
    # assessment_ratio = Ratio.get_ratio(tax_year, 'suffolk', town='100')
    assessment_ratio = 1

    time_adjustments = TimeAdjustmentValue.query.filter(
        TimeAdjustmentValue.county == 'broward').all()
    properties_rules = PropertiesRules.load_rules(
        'broward',
        town=None,
        year=assessment_date.tax_year)
    rules_controller = RulesController(properties_rules,
                                       time_adjustments=time_adjustments,
                                       valuation_date=assessment_date.valuation_date)

    for prop_id in props:
        try:
            subj = PropertyService.get_property(property_id=prop_id)
            sale_dates_from = date(day=1, month=1, year=2017)
            sale_dates_to = date(day=1, month=3, year=2020)
            print(f'subject {subj.id} apn {subj.apn}')
            cma = SingleCmaController(subj,
                                      mass_cma=True,
                                      rules_controller=rules_controller,
                                      assessment_ratio=assessment_ratio,
                                      assessment_date=assessment_date,
                                      sale_dates_from=sale_dates_from,
                                      sale_dates_to=sale_dates_to
                                      )
            cma.compute_cma()
            assmnt_values = cma.get_requested_assessment_range_values()
            total_good_comps = len(cma.get_good_comps())
            total_all_comps = len(cma.get_all_comps())
            print(f'assessment values {assmnt_values}, '
                  f'total good comps {total_good_comps}, '
                  f'total all comps {total_all_comps}')
        except (NotEnoughCompsException, SubjectLacksDataException) as e:
            print(e)


def perform_cma(row, rules_controller, use_new_attributes=False):
    from manage import app
    with app.app_context():
        q = db.session.query(Property, Owner).filter(
            Property.apn == row['ParID']).join(
            Owner,
            and_(Owner.property_id == Property.id,
                 Owner.data_source == 'assessment')
        ).first()
        if not q:
            return {
                'ParID': row['ParID'],
                'Section': row['Section'],
                'Block': row['Block'],
                'Lot': row['Lot'],
                'New Av': row['New AV']
            }
        sale_dates_from = date(day=1, month=1, year=2017)
        sale_dates_to = date(day=1, month=3, year=2020)
        assessment = Assessment(value=int(row['New AV']))

        prop = q.Property
        if use_new_attributes:
            result = db.session.execute(
                'SELECT * FROM helper.nass_sbj WHERE apn = :val',
                {'val': row['ParID']}
            ).first()
            Record = namedtuple('Record', result.keys())
            if result:
                record = Record(*result)
                prop.lot_size = record.lot_size
                prop.rooms = record.rooms
                prop.gla_sqft = record.gla_sqft
                prop.baths = record.baths
                prop.basement_type = record.basement_type
                prop.waterfront = record.waterfront
                prop.property_style = record.property_style
                prop.full_baths = record.full_baths
                prop.half_baths = record.half_baths
                prop.location = record.location

        cma = SingleCmaController(prop,
                                  mass_cma=True,
                                  rules_controller=rules_controller,
                                  sale_dates_from=sale_dates_from,
                                  sale_dates_to=sale_dates_to,
                                  assessment_ratio=0.001,
                                  subject_assessment=assessment
                                  )
        cma.compute_cma()
        assmnt_values = cma.get_requested_assessment_range_values(amount_ranges=[3, 6, 9])
        total_good_comps = len(cma.get_good_comps())
        total_all_comps = len(cma.get_all_comps())

        # saving calculation
        computed_cma = assmnt_values['misc']['3']
        saving = assessment.assessment_value - computed_cma if computed_cma else None
        # print(assmnt_values, total_good_comps, total_all_comps, saving)
        return {
            'ParID': q.Property.apn,
            'Section': row['Section'],
            'Block': row['Block'],
            'Lot': row['Lot'],
            'New Av': row['New AV'],
            'Subject Address': q.Property.address,
            # 'Legal address': prop.apn,
            'Previous Client': 'Y',
            # 'County Tentative Assessment': 'Not applicable',
            'Owner Address': ' '.join([q.Owner.owner_address_1 or '',
                                       q.Owner.owner_address_2 or '',
                                       q.Owner.owner_address_3 or '']),
            'Owner Full Name': ' '.join([
                q.Owner.first_name or '',
                q.Owner.last_name or ''
            ]),
            'Second Owner Full Name': ' '.join([
                q.Owner.second_owner_first_name or '',
                q.Owner.second_owner_last_name or ''
            ]),
            'Savings': saving,
            'Good Average 1-3': assmnt_values['good']['3'],
            'Good Average 1-6': assmnt_values['good']['6'],
            'Good Average 1-9': assmnt_values['good']['9'],
            'All Average 1-3': assmnt_values['misc']['3'],
            'All Average 1-6': assmnt_values['misc']['6'],
            'All Average 1-9': assmnt_values['misc']['9'],
            'Total Good Comparables': total_good_comps,
            'Total All Comparables': total_all_comps
        }


@bp.cli.command('custom_mass_cma')
def custom_mass_cma():
    """Run mass cma with specific New AV (new assessment values) and produce the csv output
    similar to mass cma report"""

    time_adjustments = TimeAdjustmentValue.query.filter(
        TimeAdjustmentValue.county == 'nassau').all()
    properties_rules = PropertiesRules.load_rules(
        'nassau',
        town=None,
        year=2020)
    rules_controller = RulesController(properties_rules,
                                       time_adjustments=time_adjustments,
                                       valuation_date=date(day=1, month=2, year=2020))

    target_file = DATA_IMPORT / 'src' / 'nassau' / 'custom_assessment' / 'NassauACWIN (1).csv'

    my_reader = csv.DictReader(open(target_file))
    cma_results = []

    # not async
    # pbar = tqdm(total=len(list(my_reader)))
    # # reader rewind back to the beginning
    # my_reader = csv.DictReader(open(target_file))
    # for row in my_reader:
    #     pbar.update(1)
    #     cma_result = perform_cma(row, rules_controller)
    #     cma_results.append(cma_result)
    #     print(cma_result)

    # async
    async_process(my_reader, rules_controller)

    write_results_to_csv(cma_results, file_name='NassauACWIN_result.csv')


@bp.cli.command('custom_mass_cma_with_updated_properties')
def custom_mass_cma_with_updated_properties():
    # run custom mass_cma using the custom property attributes
    time_adjustments = TimeAdjustmentValue.query.filter(
        TimeAdjustmentValue.county == 'nassau').all()
    properties_rules = PropertiesRules.load_rules(
        'nassau',
        town=None,
        year=2020)
    rules_controller = RulesController(properties_rules,
                                       time_adjustments=time_adjustments,
                                       valuation_date=date(day=1, month=2, year=2020))

    target_file = DATA_IMPORT / 'src' / 'nassau' / 'custom_assessment' / 'N19278.csv'
    my_reader = csv.DictReader(open(target_file))

    # for row in my_reader:
    #     cma_result = perform_cma(row, rules_controller, use_new_attributes=True)
    #     cma_results.append(cma_result)

    cma_results = async_process(my_reader, rules_controller)

    write_results_to_csv(cma_results, file_name='N19278_result.csv')


def async_process(reader, rules_controller):
    cma_results = []
    with ThreadPoolExecutor(MAX_WORKER_COUNT) as executor:
        futures = [executor.submit(perform_cma,
                                   row,
                                   rules_controller) for row in reader]
        print('tasks submitted')
        pbar = tqdm(total=len(list(reader)))
        for future in as_completed(futures):
            pbar.update(1)
            try:
                r = future.result()
                cma_results.append(r)
            except Exception:
                traceback.print_exc(file=sys.stdout)
    return cma_results


def write_results_to_csv(cma_results, file_name):
    """
    Write the results array into csv file
    """
    output_file = DATA_IMPORT / 'src' / 'nassau' / 'custom_assessment' / file_name
    header = ['ParID', 'Section', 'Block', 'Lot',
              'New Av', 'Subject Address', 'Previous Client',
              'Owner Address', 'Owner Full Name', 'Second Owner Full Name',
              'Savings', 'Good Average 1-3', 'Good Average 1-6',
              'Good Average 1-9', 'All Average 1-3', 'All Average 1-6',
              'All Average 1-9', 'Total Good Comparables', 'Total All Comparables']
    with open(output_file, 'w') as f:
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        for cma_result in cma_results:
            writer.writerow(cma_result)
