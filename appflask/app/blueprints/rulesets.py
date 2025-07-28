import datetime
from collections import defaultdict
from pandas.core.common import flatten

from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, abort
from flask_security import login_required
from sqlalchemy.exc import IntegrityError

from app import db
from app.database.models.property import TOWNS
from app.blueprints.forms.ruleset import (
    PropertyRuleForm,
    PropertyRuleEditForm,
    SelectionRuleForm,
    PropertyRuleFilterForm,
)
from app.database.models.user import Permission
from app.routing.decorators import permission_required
from app.rules.controllers import RulesController
from app.rules.models import PropertiesRules, InventoryRules, SelectionRules
from app.rules.obsolescence import ALL_OBSOLESCENCE
from app.settings.models import AssessmentDate
from app.utils.constants import get_all_towns, NASSAU_VILLAGES, get_nassau_villages, get_townships, County

ruleset = Blueprint('rule_set', __name__, url_prefix='/rulesets')


@ruleset.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PropertyRuleFilterForm()
    form.county.choices = [(town, town.capitalize()) for town in TOWNS.keys()]
    form.county.choices.insert(0, ('', 'Select County:'))
    form.town.choices = [(town, town) for town in get_all_towns(TOWNS)]
    form.town.choices.insert(0, ('', 'Select Township:'))

    if form.validate_on_submit() and form.apply.data:
        if not form.county.data and not form.town.data:
            pass
        else:
            rs_q = PropertiesRules.query.filter_by(county=form.county.data)
            if form.town.data:
                rs_q = rs_q.filter_by(town=form.town.data)
            properties_rules = rs_q.all()
            return render_template('rule_sets.html', properties_rules=properties_rules, form=form)
    if form.validate_on_submit() and form.clear.data:
        return redirect(request.referrer)

    properties_rules = PropertiesRules.query.order_by(
        PropertiesRules.county.desc(), PropertiesRules.town.desc()).all()
    return render_template('rule_sets.html', properties_rules=properties_rules, form=form)


@ruleset.route('/create', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def create():
    form = PropertyRuleForm()
    form.county.choices = [(town, town.capitalize()) for town in TOWNS.keys()]
    form.town.choices = [(town, town) for town in get_all_towns(TOWNS)]
    form.town.choices.append(('', 'Select Township:'))

    nv = NASSAU_VILLAGES[:]
    nv.pop(0)
    nv.pop(0)
    nv.insert(0, ('', 'Select Village'))
    form.village.choices = nv

    master_rule = PropertiesRules.query.filter(PropertiesRules.town.is_(None),
                                               PropertiesRules.county.is_(None)).first()
    if form.validate_on_submit() and form.submit.data:
        pr = None
        if form.town.data:
            pr = PropertiesRules.query.filter(PropertiesRules.county == form.county.data,
                                              PropertiesRules.town.is_(None)).first()
        parent_id = pr.id if pr else master_rule.id

        property_rule = PropertiesRules()
        property_rule.county = form.county.data
        property_rule.town = form.town.data if form.town.data else None
        property_rule.village = form.village.data if form.village.data else None
        property_rule.parent_id = parent_id

        rule_name = form.rule_name.data or f'{form.county.data.capitalize()} - {form.town.data}'
        if form.village.data:
            rule_name = f'{rule_name} - {form.village.data}'
        property_rule.rule_name = rule_name

        try:
            db.session.add(property_rule)
            db.session.flush()
        except IntegrityError:
            flash('Such property already exists')
            return render_template('rule_set_create.html', form=form)

        # check for the children:
        if not property_rule.town:
            PropertiesRules.query.filter(
                PropertiesRules.county == property_rule.county).filter(
                PropertiesRules.id != property_rule.id
            ).update({
                PropertiesRules.parent_id: property_rule.id
            })
        db.session.commit()
        flash('Rule set successfully added')
        return redirect(url_for('rule_set.index'))

    if form.validate_on_submit() and form.cancel.data:
        return redirect(url_for('rule_set.index'))

    return render_template('rule_set_create.html', form=form)


@ruleset.route('/_get_counties/')
@login_required
def _get_counties():
    """
    Ajax method for masscma page town filters.
    """
    county = request.args.get('county', type=str)
    towns = [('', 'Select Township:')]
    if TOWNS.get(county.lower()):
        towns += [(town, town) for _, town in TOWNS.get(county.lower()).items()]
    return jsonify(towns)


@ruleset.route('/_get_villages')
@login_required
def _get_villages():
    """
    Ajax method for masscma start stop form villages or townships
    """
    county = request.args.get('county', type=str)
    if county.lower() == County.NASSAU:
        nv = get_nassau_villages()
        return jsonify(nv)
    else:
        t = get_townships(TOWNS, county)
        return jsonify(t)


@ruleset.route('/_get_assessment')
@login_required
@permission_required(Permission.MASS_CMA)
def _get_assessment():
    """
    Ajax to get the assessments before we attempt to run the masscma
    """
    county = request.args.get('county', type=str)
    choices = AssessmentDate.select_field_choices(county)
    return jsonify(choices)


@ruleset.route('/_get_sale_dates')
@login_required
@permission_required(Permission.MASS_CMA)
def _get_sale_dates():
    """
    Ajax
    """
    county = request.args.get('county', type=str)

    assessment_id = request.args.get('id', type=int)
    assessment_date = AssessmentDate.query.get(assessment_id)
    year = assessment_date.tax_year

    property_rule = PropertiesRules.load_rules(county=county, year=year)
    rule_controller = RulesController(property_rule)

    date_from = rule_controller.get_value('SALE_DATE_FROM')
    date_from_str = date_from.strftime('%Y-%m-%d') if date_from else '2019-01-01'
    date_to = rule_controller.get_value('SALE_DATE_TO')
    date_to_str = date_to.strftime('%Y-%m-%d') if date_to else '2020-07-07'

    return jsonify({
        'date_from': date_from_str,
        'date_to': date_to_str
    })


@ruleset.route('/delete_property_rule/<int:pr_id>/')
@login_required
@permission_required(Permission.EDIT)
def delete_pr(pr_id):
    property_rule = PropertiesRules.query.get_or_404(pr_id)
    master_rule = PropertiesRules.query.filter(PropertiesRules.county.is_(None),
                                               PropertiesRules.town.is_(None)).first_or_404()
    if not property_rule.town:
        PropertiesRules.query.filter(
            PropertiesRules.id != master_rule.id).filter(
            PropertiesRules.county == property_rule.county
        ).update({
            PropertiesRules.parent_id: master_rule.id
        })
    db.session.delete(property_rule)
    db.session.commit()
    return redirect(url_for('rule_set.index'))


@ruleset.route('/edit/<int:pr_id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def edit(pr_id):
    rule_set = PropertiesRules.query.get_or_404(pr_id)
    form = PropertyRuleEditForm(obj=rule_set)
    form.county.choices = [(town, town.capitalize()) for town in TOWNS.keys()]
    form.county.choices.append(('', 'Select County:'))
    form.town.choices = [(town, town) for town in get_all_towns(TOWNS)]
    form.town.choices.append(('', 'Select Township:'))
    nv = NASSAU_VILLAGES[:]
    nv.pop(0)
    nv.pop(0)
    nv.insert(0, ('', 'Select Village'))
    form.village.choices = nv
    if form.validate_on_submit() and form.save.data:
        town = rule_set.town or ''
        county = rule_set.county or ''
        if rule_set.rule_name == county + ' - ' + town and form.rule_name.data == rule_set.rule_name:
            rule_set.rule_name = form.county.data + ' - ' + form.town.data
        else:
            rule_set.rule_name = form.rule_name.data
        rule_set.town = form.town.data or None
        rule_set.village = form.village.data or None
        rule_set.adjustments_all = form.adjustments_all.data
        rule_set.adjustments_required = form.adjustments_required.data
        rule_set.last_updated = datetime.datetime.now()
        db.session.add(rule_set)
        db.session.commit()
        flash('The rule set has been updated.')
        return redirect(url_for('rule_set.index'))
    if form.validate_on_submit() and form.cancel.data:
        return redirect(url_for('rule_set.index'))
    if form.validate_on_submit() and form.delete.data:
        return delete_pr(rule_set.id)
    form.rule_name.data = rule_set.rule_name
    form.town.data = rule_set.town or ''
    form.county.data = rule_set.county or ''
    form.adjustments_all.data = ",".join(rule_set.adjustments_all or '')
    form.adjustments_required.data = ','.join(rule_set.adjustments_required or '')
    form.pr_id.data = rule_set.id

    srf = SelectionRuleForm()
    if srf.validate_on_submit() and srf.submit_sr.data:
        sr = rule_set.selection_rules or SelectionRules()
        sr.parent_id = rule_set.id
        sr.proximity_range = srf.proximity_range.data
        sr.sale_date_from = srf.sale_date_from.data
        sr.sale_date_to = srf.sale_date_to.data
        sr.percent_gla_lower = srf.percent_gla_lower.data
        sr.percent_gla_higher = srf.percent_gla_higher.data
        sr.percent_lot_size_lower = srf.percent_lot_size_lower.data
        sr.percent_lot_size_higher = srf.percent_lot_size_higher.data
        sr.percent_sale_lower = srf.percent_sale_lower.data
        sr.percent_sale_higher = srf.percent_sale_higher.data
        sr.same_property_class = None if srf.same_property_class_included.data else srf.same_property_class.data
        sr.same_one_family_types = None if srf.same_one_family_types_included.data else srf.same_one_family_types.data
        sr.same_school_district = None if srf.same_school_district_included.data else srf.same_school_district.data
        sr.same_town = None if srf.same_town_included.data else srf.same_town.data
        sr.same_street = None if srf.same_street_included.data else srf.same_street.data
        sr.same_property_style = None if srf.same_property_style_included.data else srf.same_property_style.data
        db.session.add(sr)
        rule_set.last_updated = datetime.datetime.now()
        db.session.commit()
        return redirect(url_for('rule_set.index'))

    if rule_set.selection_rules:
        c = RulesController(rule_set)
        sr = rule_set.selection_rules
        srf = SelectionRuleForm(obj=rule_set.selection_rules)
        srf.proximity_range_included.data = False if srf.proximity_range.data else True
        srf.proximity_range_inherited.data = c.get_inherited_selection_rule('RANGE')[2]

        srf.sale_date_from_included.data = False if srf.sale_date_from.data else True
        srf.sale_date_from_inherited.data = c.get_inherited_selection_rule(
            'SALE_DATE_FROM')[2]
        srf.sale_date_to_included.data = False if srf.sale_date_to.data else True
        srf.sale_date_to_inherited.data = c.get_inherited_selection_rule(
            'SALE_DATE_TO')[2]
        srf.percent_gla_lower_included.data = False if srf.percent_gla_lower.data else True
        srf.percent_gla_lower_inherited.data = c.get_inherited_selection_rule(
            'PERCENT_GLA_LOWER')[2]
        srf.percent_gla_higher_included.data = False if srf.percent_gla_higher.data else True
        srf.percent_gla_higher_inherited.data = c.get_inherited_selection_rule(
            'PERCENT_GLA_HIGHER')[2]
        srf.percent_lot_size_lower_included.data = False if srf.percent_lot_size_lower.data else True
        srf.percent_lot_size_lower_inherited.data = c.get_inherited_selection_rule(
            'PERCENT_LOT_SIZE_LOWER')[2]
        srf.percent_lot_size_higher_included.data = False if srf.percent_lot_size_higher.data else True
        srf.percent_lot_size_higher_inherited.data = c.get_inherited_selection_rule(
            'PERCENT_LOT_SIZE_HIGHER')[2]
        srf.percent_sale_lower_included.data = False if srf.percent_sale_lower.data else True
        srf.percent_sale_lower_inherited.data = c.get_inherited_selection_rule(
            'PERCENT_SALE_LOWER')[2]
        srf.percent_sale_higher_included.data = False if srf.percent_sale_higher.data else True
        srf.percent_sale_higher_inherited.data = c.get_inherited_selection_rule(
            'PERCENT_SALE_HIGHER')[2]
        srf.same_property_class.data = sr.same_property_class
        srf.same_property_class_included.data = False if sr.same_property_class is not None else True
        srf.same_property_class_inherited.data = c.get_inherited_selection_rule(
            'SAME_PROPERTY_CLASS')[2]
        srf.same_school_district_included.data = False if sr.same_school_district is not None else True
        srf.same_school_district_inherited.data = c.get_inherited_selection_rule(
            'SAME_SCHOOL_DISTRICT')[2]
        srf.same_town_included.data = False if sr.same_town is not None else True
        srf.same_town_inherited.data = c.get_inherited_selection_rule(
            'SAME_TOWN')[2]
        srf.same_street_included.data = False if sr.same_street is not None else True
        srf.same_street_inherited.data = c.get_inherited_selection_rule(
            'SAME_STREET')[2]
        srf.same_property_style_included.data = False if sr.same_property_style is not None else True
        srf.same_property_style_inherited.data = c.get_inherited_selection_rule(
            'SAME_PROPERTY_STYLE')[2]
        srf.same_one_family_types_included.data = False if sr.same_one_family_types is not None else True
        srf.same_one_family_types_inherited.data = c.get_inherited_selection_rule(
            'SAME_ONE_FAMILY_TYPES')[2]

    return render_template('rule_settings.html', rule_set=rule_set,
                           sr_form=srf, form=form)


@ruleset.route('/edit_obs/<int:rs_id>', methods=['POST'])
@login_required
@permission_required(Permission.EDIT)
def edit_obs(rs_id):
    rule_set = PropertiesRules.query.get_or_404(rs_id)
    if request.form.get('cancel_ob'):
        return redirect(url_for('rule_set.index'))
    obsolescence = []
    for ob_name, ob_dict in ALL_OBSOLESCENCE[rule_set.county].items():
        adjustment = request.form.get(str(ob_dict['rule_index'])) or 0
        obsolescence.append(float(adjustment) or None)
    rule_set.obsolescence_rules = obsolescence
    db.session.commit()
    return redirect(url_for('rule_set.index'))


@ruleset.route('/edit_ir/<int:rs_id>', methods=['POST'])
@login_required
@permission_required(Permission.EDIT)
def edit_ir(rs_id):
    pr = PropertiesRules.query.get_or_404(rs_id)
    if request.form.get('cancel_ir'):
        return redirect(url_for('rule_set.index'))

    if request.form.get('save_ir'):
        # grab and arrange all data coming from the form
        form_data = defaultdict(dict)
        for key, value in request.form.items():
            if len(key.split('ir_id')) > 1:
                key_sp = key.split('ir_id')
                form_data[key_sp[1]][key_sp[0]] = int(value) if value else None
            if len(key.split('_basement_')) > 1:
                key_sp = key.split('_basement_')
                try:
                    form_data[key_sp[1]][key_sp[0]].append(int(value) if value else None)
                except KeyError:
                    form_data[key_sp[1]][key_sp[0]] = []
                    form_data[key_sp[1]][key_sp[0]].append(int(value) if value else None)
            if key.endswith('_new_ir'):
                form_data['new'][key.replace('_new_ir', '')] = int(value) if value else None
            if key.endswith('new_basement'):
                try:
                    form_data['new']['basement_prices'].append(int(value) if value else None)
                except KeyError:
                    form_data['new']['basement_prices'] = []
                    form_data['new']['basement_prices'].append(int(value) if value else None)

        # persist new row if these is any new record
        new_ir = form_data.pop('new')
        if any(list(flatten(new_ir.values()))):
            new_inventory_rule = InventoryRules(**new_ir)
            new_inventory_rule.parent_id = pr.id
            db.session.add(new_inventory_rule)

        # update database with grabbed data
        for key, value in form_data.items():
            InventoryRules.query.filter_by(id=key).update(value)
        db.session.commit()
        return redirect(url_for('rule_set.index'))
    return abort(404)


@ruleset.route('/delete_inventory_rule/<int:ir_id>/')
@login_required
@permission_required(Permission.EDIT)
def delete_ir(ir_id):
    property_rule_id = request.args.get('pr_id')
    inventory_rule = InventoryRules.query.get_or_404(ir_id)
    db.session.delete(inventory_rule)
    db.session.commit()
    return redirect(url_for('rule_set.edit', pr_id=property_rule_id, _anchor='inv_adj'))
