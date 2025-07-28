import copy
import datetime
from decimal import Decimal
from app.rules.adjustments import Adjustment
from app.rules.models import ALL_ADJUSTMENTS, ALL_RULES, RULE_INVENTORY, RULE_MISC, PropertiesRules
from app.rules.obsolescence import RULE_OBSOLESCENCE, get_index_from_code, get_name_from_code, get_code_from_idx
from app.rules.selections import ALL_SELECTIONS, Selection
from app.settings.models import TimeAdjustmentValue
from app.utils.constants import County


class RulesController(object):
    rules = None
    time_adjustments = None
    valuation_date = None

    def __init__(self, rules: PropertiesRules, time_adjustments=None,
                 valuation_date=None):
        self.rules = rules
        self.time_adjustments = time_adjustments
        self.valuation_date = valuation_date

    def get_time_adjustments(self):
        if not self.time_adjustments:
            county = self.rules.county
            self.time_adjustments = TimeAdjustmentValue.query.filter(TimeAdjustmentValue.county == county.lower()).all()
        return self.time_adjustments

    def adjust_property(self, subject, prop):
        """
        Returns grand total of adjustments and details on each adjustments
        """
        status = True
        messages = []
        results = []
        # obso_results = None

        all_adjustments = sorted(ALL_ADJUSTMENTS.items(), key=lambda adj: adj[1]['order'])
        rule_adjustments = self.get_all_adjustments()

        for adjustment in all_adjustments:
            adjustment_key = adjustment[0]

            if adjustment_key in rule_adjustments:
                # process obsolescence adjustment differently
                # if adjustment_key == Adjustment.LOCATION and subject.county in County.get_florida_counties():
                #     obso_results = self.adjust_obso(adjustment_key, subject, prop)
                #     if obso_results:
                #         results.append(obso_results)
                # else:
                results.append(self.adjust(adjustment_key, subject, prop))

        grand_total = prop.other_adjustment if prop.other_adjustment else 0
        required_adjs = self.get_required_adjustments()
        for adjustment in results:
            if adjustment['adjusted']:
                # do not include 'COS' adjustment to grand_total for the Florida counties
                if adjustment['key'] == Adjustment.COST_OF_SALE and prop.county in County.get_florida_counties():
                    prop.adjustment_delta_value_cos = adjustment['value']
                    continue
                else:
                    grand_total += adjustment['value']

            elif adjustment['name'] in required_adjs:
                status = False
                messages.append("Failed Required adjustment: {}".format(adjustment['name']))

        return status, grand_total, results, messages

    # def adjust_obso_helper(self, subject_land_uses, county, price, rule_value, location_code):
    #     max_index = get_index_from_code(county, int(location_code))
    #     max_value = rule_value[max_index]
    #     max_code = int(location_code)
    #     for code in subject_land_uses:
    #         index_ = get_index_from_code(county, code)
    #         value_ = rule_value[index_]
    #         if value_ > max_value:
    #             max_value = value_
    #             max_code = code
    #     obso = dict(
    #         obs_name=get_value_from_code(county, max_code)['rule_name'],
    #         value=float(max_value),
    #         price_change=price * max_value / 100
    #     )
    #     return obso

    # def adjust_obso(self, adjustment, subject, prop):
    #     # results calculated based on location column.
    #     # location column for now defines only the ocean view
    #     location_results = self.adjust(adjustment, subject, prop)
    #
    #     # now we retrieve what is calculated from the land_use column
    #     # florida properties may have multiple obsolescences
    #     subject_land_uses = [obs.obs.land_use for obs in subject.obsolescences]
    #     comp_land_uses = [obs.obs.land_use for obs in prop.obsolescences]
    #
    #     rule_value = location_results['rule_set_used'].obsolescence_rules
    #
    #     subject_obso = self.adjust_obso_helper(subject_land_uses,
    #                                            prop.county,
    #                                            prop.last_sale_price,
    #                                            rule_value,
    #                                            location_results['subject_value'])
    #
    #     comp_obso = self.adjust_obso_helper(comp_land_uses,
    #                                         prop.county,
    #                                         prop.last_sale_price,
    #                                         rule_value,
    #                                         location_results['comp_value'])
    #
    #     # result = float((subject_value - comp_value) / 100) * prop.last_sale_price
    #     # adjusted_value = (location_results['value'] or 0) + result
    #     adjusted_value = (comp_obso['value'] - subject_obso['value']) * prop.last_sale_price / 100
    #
    #     return {
    #         'key': adjustment,
    #         'adjusted': True if adjusted_value else False,
    #         'value': adjusted_value,
    #         'name': location_results['name'],
    #         'rule_value': str(rule_value),
    #         'subject_value': str(subject_obso['value']),
    #         'comp_value': str(comp_obso['value']),
    #         'subject_obsolescences': subject_obso,
    #         'comp_obsolescences': comp_obso
    #     }

    def adjust(self, adjustment, subject, prop):
        """
        Does adjustment and returns dict with information:
        adjusted: True/False
        value: Adjustment Value
        name: Adjustment Name
        rule: The rule that was used
        rule_value: The value of the rule
        """

        price = prop.last_sale_price

        # to find the correct inventory rule use sbj market value instead of comp last sale
        rule_set_used, rule_used, rule_value = self.get_rule_for(
            adjustment,
            price=subject.market_value)

        if rule_value is None:
            # No matching rule available
            results = {
                'key': adjustment,
                'adjusted': False,
                'name': adjustment,
                'error': True,
                'status': 'No Matching rule for {} adjustment of {} subject'.format(adjustment, subject),
            }
            return results

        adjustment_info = ALL_ADJUSTMENTS[adjustment]

        # Define the values we'll forward to the rule
        subject_value = None
        comp_value = None
        if 'property_field' in adjustment_info:
            subject_value = getattr(subject, adjustment_info['property_field'])
            comp_value = getattr(prop, adjustment_info['property_field'])

        if 'subject_value_method' in adjustment_info:
            subject.valuation_date = self.valuation_date
            subject.rule_value = rule_value
            subject_value = adjustment_info['subject_value_method'](subject)
        if 'comp_value_method' in adjustment_info:
            prop.rule_value = rule_value
            comp_value = adjustment_info['comp_value_method'](prop)

        # do the adjustments and get adjustments results
        # can be None if subject or comparable can't be adjusted for any reason
        # or dict object with 'adjusted_value'
        # and optional 'percent_value_difference'
        adjustment_results = adjustment_info['adjustment_class']().adjust(
            subject_value,
            comp_value,
            rule_value,
            price
        )

        adjusted_value = None
        comp_percent_value = None
        subject_percent_value = None

        if adjustment_results:
            adjusted_value = adjustment_results.get('adjusted_value')
            comp_percent_value = adjustment_results.get('comp_percent_value')
            subject_percent_value = adjustment_results.get('subject_percent_value')

        subject_rule_value = ''
        if adjustment == 'LOCATION':
            # expand subject and comparable with new attribute obs.
            # This is the max value obsolescence subject affected by

            # avoiding circular imports
            from app.utils.gis_utils import convert_wkb_to_geojson

            subject.obs_geojson = convert_wkb_to_geojson(
                obs_name=get_name_from_code(subject.county, subject_value[0]),
                wkb_list=subject_value[1])
            prop.obs_geojson = convert_wkb_to_geojson(
                obs_name=get_name_from_code(prop.county, comp_value[0]),
                wkb_list=comp_value[1])

            # subject_value and comp_value are tuples of code and geometry
            subject_value = subject_value[0]
            comp_value = comp_value[0]
            idx = get_index_from_code(prop.county, subject_value)
            try:
                subject_rule_value = rule_value[0][idx]
                subject_rule_value = f'{int(Decimal(subject_rule_value))}%'
                subject_value = get_code_from_idx(subject.county, idx)
            except Exception:
                subject_value = None
                subject_rule_value = '0%'

            idx = get_index_from_code(prop.county, comp_value)
            try:
                rule_value = rule_value[0][idx]
                rule_value = f'{int(Decimal(rule_value))}%'
                comp_value = get_code_from_idx(prop.county, idx)
            except Exception:
                # in case some error with index or the decimal conversion
                # set rule value to empty string
                rule_value = '0%'
                comp_value = None

        results = {
            'key': adjustment,
            'adjusted': not (adjusted_value is None),
            'value': adjusted_value,
            'comp_percent_value': comp_percent_value,
            'subject_percent_value': subject_percent_value,
            'name': adjustment_info['name'],
            'inventory_rule_id': rule_used.id if rule_used else None,  # None when adjusting TIME
            'rule_value': str(rule_value),  # comp rule value
            'subject_rule_value': str(subject_rule_value),
            'subject_value': str(subject_value) if subject_value else None,
            'comp_value': str(comp_value) if comp_value else None,
            'rule_set_used': rule_set_used
        }
        return results

    def get_inherited_param(self, param_name, rules=None):
        if not rules:
            rules = self.rules

        value = getattr(rules, param_name)
        # TODO: Disabled Inheritance
        # if not value and rules.parent:
        #     return self.get_inherited_param(param_name, rules.parent)
        return value

    def get_selection_rules(self):
        return self.get_inherited_param('selection_rules')

    def get_all_adjustments(self, rules=None):
        value = self.get_inherited_param('adjustments_all')
        return value or []

    def get_required_adjustments(self, rules=None):
        value = self.get_inherited_param('adjustments_required')
        return value or []

    def get_all_rules(self, rules=None):
        if not rules:
            rules = self.rules
        rules_list = [rules]
        # Recursive magic

        # TODO: Disable inheritance for time being
        # if rules and rules.parent:
        #     rules_list.extend(self.get_all_rules(rules.parent))
        return [r for r in rules_list if r]

    def get_value(self, rule_name, price=None):
        # Simplified method that returns only the value and no other information
        return self.get_rule_for(rule_name, price=price)[2]

    def get_date_range(self):
        enabled = False
        min_date = datetime.datetime(year=1950, month=1, day=1).date()
        max_date = datetime.datetime.now().date()

        sale_date_from = self.get_value(Selection.SALE_DATE_FROM)
        if sale_date_from:
            enabled = True
            min_date = sale_date_from

        sale_date_to = self.get_value(Selection.SALE_DATE_TO)
        if sale_date_to:
            enabled = True
            max_date = sale_date_to

        return min_date, max_date, enabled

    def get_proximity_in_meters(self):
        meters = float(self.get_value(Selection.PROXIMITY_RANGE)) * 1609.0  # 1609 is meters in 1 mile
        return meters

    def get_rule_for(self, rule_name, price=0):
        """
        Critical and hard to follow logic code.
        If you are not sure what each line means, you probably don't want to tweak it.

        The short-version pseudocode to help code inspection:

        all_rules = "county+town" rules + "county" rules + "town" rules. Order is important

        iterating through this list:
            if this rules_set has a rule record, and value is not None, then we use it.
            Otherwise go to a next "parent" rule_set in hopes it will have what we need.

        In other words, we try getting what we need, otherwise ask if the parent has it.

        Returns a tuple of:
        - rule_set that was used
        - rule - a specific rule of this rule_set we used
        - value - the value of this rule for use in formulas
        """

        rule_meta_info = ALL_RULES[rule_name]
        rule_type = rule_meta_info['rule_type']

        all_rules = self.get_all_rules()

        return_rule_set = None
        return_rule = None
        return_value = None

        # Logic for selecting exact rule to be used differs for rule types
        if rule_type == RULE_INVENTORY:
            field_name = rule_meta_info['rule_field']
            # Need to check price range
            for rules_set in all_rules:
                # We have to find the rule that specifically matches the price
                price_matched_rule = None
                for inventory_rule in getattr(rules_set, rule_type):
                    if (price >= inventory_rule.price_start) and (price <= inventory_rule.price_end):
                        price_matched_rule = inventory_rule
                        break
                if price_matched_rule and not getattr(price_matched_rule, field_name) is None:
                    # Amazing, price matched and the value is not None
                    return_rule_set = rules_set
                    return_rule = price_matched_rule
                    return_value = getattr(price_matched_rule, field_name)
                    break

        elif rule_type == RULE_OBSOLESCENCE:
            for rules_set in all_rules:
                # we need to know the county for obsolescence for that returning tuple
                return_value = getattr(rules_set, rule_type), rules_set.county
                if return_value:
                    return_rule_set = rules_set
                    return_rule = None
                    break

        elif rule_type == RULE_MISC:
            # Unique rules that do not fall into other categories
            for rules_set in all_rules:
                if rule_name == Adjustment.TIME:
                    return_value = self.get_time_adjustments()
                    if return_value:
                        return_rule = None
                        return_rule_set = rules_set
                        break
                else:  # for HIGH_SALE_DATE_LOWER and HIGH_SALE_DATE_HIGHER
                    rule_field = rule_meta_info['rule_field']
                    return_value = getattr(rules_set, rule_field)
                    if return_value:
                        return_rule_set = rules_set
                        return_rule = None
                        break
        else:
            field_name = rule_meta_info['rule_field']
            for rules_set in all_rules:
                rule = getattr(rules_set, rule_type)
                if rule:
                    if not (getattr(rule, field_name) is None):
                        return_rule_set = rules_set
                        return_rule = rule
                        return_value = getattr(rule, field_name)
                        break
        return return_rule_set, return_rule, copy.copy(return_value)

    def get_inherited_selection_rule(self, rule_name):
        rule_meta_info = ALL_SELECTIONS[rule_name]
        rule_type = rule_meta_info['rule_type']  # 'selection_rules'
        all_rules = self.get_all_rules()
        all_parent_rules = [r for r in all_rules if r.id != self.rules.id]

        field_name = rule_meta_info['rule_field']
        for rules_set in all_parent_rules:
            rule = getattr(rules_set, rule_type)
            if rule:
                if not (getattr(rule, field_name) is None):
                    return rules_set, rule, getattr(rule, field_name)
        return None, None, None
