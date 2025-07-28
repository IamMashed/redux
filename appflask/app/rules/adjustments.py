from abc import ABC, abstractmethod
from collections import OrderedDict

import numpy as np
import pandas as pd

from app.rules.obsolescence import RULE_OBSOLESCENCE, get_index_from_code,\
    FLORIDA_LOCATION_OBSO_CODES, get_code_from_name
from app.utils.constants import SqftInAcre, County

RULE_INVENTORY = 'inventory_rules'
RULE_MISC = 'misc_rules'


def prop_assessment_date(prop):
    """valuation_date is added to the property at the time we do time adjustment.
        This property initially not defined in the property class
    """
    return prop.valuation_date


def prop_sale_date(prop):
    return prop.last_sale.date


def prop_location(prop):
    # code value in obsolescences focused calculations
    location = (prop.location, [])
    obs_list, county = prop.rule_value
    if prop.county in County.get_florida_counties() \
            and prop.location not in FLORIDA_LOCATION_OBSO_CODES.values():
        location = (0, [])

    # obs.obs.gis is a relationship that will return list since
    # property may consists of multiple building and that causes multiple polygons
    # in property_gis table
    if prop.county in County.get_florida_counties():
        land_uses = [(obs.obs.land_use, obs.obs.gis) for obs in prop.obsolescences]
    else:
        land_uses = [(obs.obs.property_class, obs.obs.gis) for obs in prop.obsolescences]
    roads = [(r.road.type, [r.road.geometry]) for r in prop.roads]
    # get road codes
    road_codes = [(get_code_from_name(prop.county, r[0]), r[1]) for r in roads]
    road_codes = [r for r in road_codes if r[0]]  # clear the none values
    # get the code with maximum percentage obsolescence
    max_result = location
    max_value = float('-inf')
    for code in [location, *land_uses, *road_codes]:
        index_ = get_index_from_code(county, code[0])
        if not index_:
            continue
        value_ = obs_list[index_]
        if float(value_) > max_value:
            max_result = code
    return max_result


def prop_road_obs(prop):
    pass


def property_last_sale_price(prop):
    if hasattr(prop, 'last_sale_price'):
        return prop.last_sale_price

    if prop.last_sale:
        return prop.last_sale.price
    return None


def get_property_age(prop):
    """
    Get property effective age is available or age
    """
    if prop.effective_age:
        return prop.effective_age
    return prop.age


def get_property_water_category(prop):
    return prop.water_category


def get_condo_view_floor(prop):
    """
    Get property condo view floor
    """
    return prop.condo_view_floor


class Adjustment(ABC):
    """ Abstract class for adjustments to implement """

    GLA = 'GLA'
    UNDER_AIR_GLA = 'UNDER_AIR_GLA'
    LOT = 'LOT'
    FULL_BATH = 'FULL_BATH'
    HALF_BATH = 'HALF_BATH'
    BEDROOMS = 'BEDROOMS'
    POOL = 'POOL'
    PATIO_TYPE = 'PATIO'
    PAVING_TYPE = 'PAVING'
    PORCH_TYPE = 'PORCH'
    HEAT_TYPE = 'HEAT'
    GARAGE = 'GARAGE'
    BASEMENT = 'BASEMENT'
    TIME = 'TIME_ADJ'
    LOCATION = 'LOCATION'
    ROAD = 'ROAD'
    COST_OF_SALE = 'COST_OF_SALE'
    WATER = 'WATER'
    AGE = 'AGE'
    FIREPLACE = 'FIREPLACE'
    CONDO_VIEW_FLOOR = 'CONDO_VIEW_FLOOR'

    @abstractmethod
    def adjust(self, subject_property, comparative_property, adjustment_configuration, comp_price):
        pass

    def valid_data(self, *args):
        """
        Validate input data. Check whether value is None
        :param args: The tuple of arguments to validate
        """
        for arg in args:
            if arg is None:
                return False

        return True


class AdjustmentObs(Adjustment):
    def adjust(self, subject_value, comp_value, config, comp_price):
        subject_value = subject_value[0]
        comp_value = comp_value[0]

        obs_list, county = config

        if not self.valid_data(obs_list, comp_price):
            return None

        try:
            subject_index = get_index_from_code(county, subject_value or 0)
            subject_value = obs_list[subject_index]
        except TypeError:
            subject_value = 0

        try:
            comp_index = get_index_from_code(county, comp_value or 0)
            comp_value = obs_list[comp_index] if comp_index else 0
        except TypeError:
            comp_value = 0

        adjustment_results = {'adjusted_value': float((comp_value - subject_value) / 100) * comp_price}
        return adjustment_results


class AdjustmentTime(Adjustment):
    # Adjustment in % based on the time difference
    def adjust(self, subject_property, comparative_property, time_objects, comp_price):
        """
        subject_property: date of subject assessment
        comparative_property: date of comparative property last sale
        """
        # store string date so we can pop it out later
        comparative_date = comparative_property.strftime('%Y-%m')
        # get all months with years between two dates
        reversed_ = False
        if subject_property < comparative_property:
            comparative_property, subject_property = subject_property, comparative_property
            reversed_ = True
        month_list = pd.date_range(comparative_property, subject_property,
                                   freq='MS').strftime("%Y-%m").tolist()
        # pop the comparative date for more precise coefficient calculation.
        try:
            month_list.remove(comparative_date)
        except ValueError:
            pass

        if not month_list:
            return 0
        # filter months if database contain month record
        percents = dict()
        for to in time_objects:
            to_str = f'{to.year}-{str(to.month).rjust(2, "0")}'
            if to_str in month_list:
                percents[to_str] = to.value
        multipliers = [d / 100 + 1 for d in percents.values()]

        # calculate final coefficient
        coeff = np.prod(multipliers)

        # divide or multiply based on subject assessment date later or earlier than comp sale date
        adjustment_results = {
            'adjusted_value': comp_price * coeff - comp_price if not reversed_ else comp_price / coeff - comp_price
        }

        return adjustment_results


class AdjustmentDiff(Adjustment):
    # Adjustment based on the difference in quantity of the given inventory
    def adjust(self, subject_value, comp_value, config, *_):
        if not self.valid_data(subject_value, comp_value):
            return None
        adjustment_results = {'adjusted_value': int((subject_value - comp_value) * config)}
        return adjustment_results


class AdjustmentDiffSqft(Adjustment):
    # Adjustment based on the difference in quantity of the given inventory
    def adjust(self, subject_value, comp_value, config, *_):
        if not self.valid_data(subject_value, comp_value) or not subject_value or not comp_value:
            return None

        adjustment_results = {'adjusted_value': int((subject_value - comp_value) * config)}
        return adjustment_results


class AdjustmentCostOfSale(Adjustment):
    def adjust(self, subject_value, comp_value, config, *_):
        # config is a % to adjust comparative sale price, can not be = 0
        if not self.valid_data(comp_value) or config == 0:
            return None
        adjustment_results = {'adjusted_value': int(-1 * comp_value * config / 100)}
        return adjustment_results


class AdjustmentAge(Adjustment):
    """
    Property age adjustment
    """
    def adjust(self, subject_value, comp_value, config, comp_price):
        if not self.valid_data(subject_value, comp_value) or config == 0 or config is None:
            return None

        # get year difference
        year_difference = subject_value - comp_value

        adjustment_results = {
            'adjusted_value': int((year_difference * config * comp_price) / 100),
            'comp_percent_value': year_difference * config
        }
        return adjustment_results


class AdjustmentWater(Adjustment):
    def adjust(self, subject_value, comp_value, config, comp_price):

        # can not adjust
        if config == 0 or (not subject_value and not comp_value):
            return None

        if subject_value and comp_value:
            coeff = 0
        elif not subject_value:
            coeff = -1
        else:
            coeff = 1

        subject_percent_value = config if subject_value else 0
        comp_percent_value = config if comp_value else 0

        adjustment_results = {
            'adjusted_value': int((coeff * config * comp_price) / 100),
            'subject_percent_value': subject_percent_value,
            'comp_percent_value': comp_percent_value,
        }

        return adjustment_results


class AdjustCondoViewFloor(Adjustment):
    def adjust(self, subject_value, comp_value, config, comp_price):
        # can not adjust
        if not self.valid_data(subject_value, comp_value) or config == 0 or config is None:
            return None

        # some of 'condo_view_floor' can be strings like 'GA', 'RO' etc
        # they can't be adjusted, only digits supposed to be adjusted
        if not subject_value.isdigit() or not comp_value.isdigit():
            return None

        # get the difference
        difference = int(subject_value) - int(comp_value)
        adjustment_results = {
            'adjusted_value': int((difference * config * comp_price) / 100),
            'comp_percent_value': difference * config
        }
        return adjustment_results


class AdjustmentDiffAcresToSqft(Adjustment):
    def adjust(self, subject_value, comp_value, config, *_):
        if not self.valid_data(subject_value, comp_value) or not subject_value or not comp_value:
            return None

        adjustment_results = {'adjusted_value': int((subject_value - comp_value) * config * SqftInAcre)}
        return adjustment_results


class AdjustmentMap(Adjustment):
    # Adjustment based on mapped value from config for this inventory
    def adjust(self, subject_value, comp_value, config, *_):
        if not self.valid_data(subject_value, comp_value) or not config:
            return None

        adjustment_results = {'adjusted_value': int(config[int(subject_value)] - config[int(comp_value)])}
        return adjustment_results


class AdjustmentBoolType(Adjustment):
    """
    Adjustment is based on checking the identity of subject & comparative type
    """

    def adjust(self, subject_value, comp_value, config, *_):
        if not self.valid_data(subject_value, comp_value):
            return None

        # convert boolean to int and get difference
        adjustment_results = {'adjusted_value': int((subject_value * 1 - comp_value * 1) * config)}
        return adjustment_results


"""
All adjustments meta data:
    * name: The display name of adjustment
    * rule_type: The rule type (Selection, Obsolescence, Inventory, Misc)
    * rule_field: The column name in a 'inventory_rules' if any
    * property_field: The column name in a 'property' table if any
    * adjustment_class: The class handler that do adjustment
    * subject_value_method: The method, returns a subject value
    * comp_value_method: The method, returns a comparative value
"""
ALL_ADJUSTMENTS = OrderedDict([
    (Adjustment.UNDER_AIR_GLA, {
        'name': 'Under Air GLA',
        'rule_type': RULE_INVENTORY,
        'rule_field': 'under_air_gla_sqft',
        'property_field': 'under_air_gla_sqft',
        'adjustment_class': AdjustmentDiff,
        'order': 0
    }),
    (Adjustment.GLA, {
        'name': 'GLA (SF)',
        'rule_type': RULE_INVENTORY,
        'rule_field': 'gla_sqft',
        'property_field': 'gla_sqft',
        # 'adjustment_class': AdjustmentDiff,
        'adjustment_class': AdjustmentDiffSqft,
        'order': 1
    }),
    (Adjustment.LOT, {
        'name': 'Lot (Acres/Sf)',
        'rule_type': RULE_INVENTORY,
        'rule_field': 'lot_sqft',
        'property_field': 'lot_size',
        'adjustment_class': AdjustmentDiffAcresToSqft,
        'order': 2
    }),
    (Adjustment.FULL_BATH, {
        'name': 'Full Baths',
        'rule_type': RULE_INVENTORY,
        'rule_field': 'full_bath',
        'property_field': 'full_baths',
        'adjustment_class': AdjustmentDiff,
        'order': 3
    }),
    (Adjustment.HALF_BATH, {
        'name': 'Half Baths',
        'rule_type': RULE_INVENTORY,
        'rule_field': 'half_bath',
        'property_field': 'half_baths',
        'adjustment_class': AdjustmentDiff,
        'order': 4
    }),
    (Adjustment.FIREPLACE, {
        'name': 'Fireplace',
        'rule_type': RULE_INVENTORY,
        'rule_field': 'fireplace',
        'property_field': 'fireplaces',
        'adjustment_class': AdjustmentDiff,
        'order': 5
    }),
    (Adjustment.BEDROOMS, {
        'name': 'Beds',
        'rule_type': RULE_INVENTORY,
        'rule_field': 'bedrooms',
        'property_field': 'bedrooms',
        'adjustment_class': AdjustmentDiff,
        'order': 6
    }),
    (Adjustment.POOL, {
        'name': 'Pool',
        'rule_type': RULE_INVENTORY,
        'rule_field': 'pool',
        'property_field': 'pool',
        'adjustment_class': AdjustmentBoolType,
        'order': 7
    }),
    (Adjustment.PATIO_TYPE, {
        'name': 'Patio Type',
        'rule_type': RULE_INVENTORY,
        'rule_field': 'patio_type_prices',
        'property_field': 'patio_type',
        'adjustment_class': AdjustmentMap,
        'order': 8
    }),
    (Adjustment.PAVING_TYPE, {
        'name': 'Paving Type',
        'rule_type': RULE_INVENTORY,
        'rule_field': 'paving_type_prices',
        'property_field': 'paving_type',
        'adjustment_class': AdjustmentMap,
        'order': 9
    }),
    (Adjustment.PORCH_TYPE, {
        'name': 'Porch Type',
        'rule_type': RULE_INVENTORY,
        'rule_field': 'porch_type_prices',
        'property_field': 'porch_type',
        'adjustment_class': AdjustmentMap,
        'order': 10
    }),
    (Adjustment.HEAT_TYPE, {
        'name': 'Heat Type',
        'rule_type': RULE_INVENTORY,
        'rule_field': 'heat_type_prices',
        'property_field': 'heat_type',
        'adjustment_class': AdjustmentMap,
        'order': 11
    }),
    (Adjustment.GARAGE, {
        'name': 'Garage',
        'rule_type': RULE_INVENTORY,
        'rule_field': 'garage',
        'property_field': 'garages',
        'adjustment_class': AdjustmentDiff,
        'order': 12
    }),
    (Adjustment.BASEMENT, {
        'name': 'Basement',
        'rule_type': RULE_INVENTORY,
        'rule_field': 'basement_prices',
        'property_field': 'basement_type',
        'adjustment_class': AdjustmentMap,
        'order': 13
    }),
    (Adjustment.TIME, {
        'name': 'Time Adj',
        'rule_type': RULE_MISC,
        'adjustment_class': AdjustmentTime,
        'subject_value_method': prop_assessment_date,
        'comp_value_method': prop_sale_date,
        'order': 14
    }),
    (Adjustment.LOCATION, {
        'name': 'Location Adj',
        'rule_type': RULE_OBSOLESCENCE,
        'adjustment_class': AdjustmentObs,
        'subject_value_method': prop_location,
        'comp_value_method': prop_location,
        'order': 15
    }),
    (Adjustment.COST_OF_SALE, {
        'name': 'Cost Of Sale',
        'rule_type': RULE_MISC,
        'rule_field': 'cost_of_sale',
        'subject_value_method': property_last_sale_price,
        'comp_value_method': property_last_sale_price,
        'adjustment_class': AdjustmentCostOfSale,
        'order': 16
    }),
    (Adjustment.AGE, {
        'name': 'Age',
        'rule_type': RULE_MISC,
        'rule_field': 'age',
        'subject_value_method': get_property_age,
        'comp_value_method': get_property_age,
        'adjustment_class': AdjustmentAge,
        'order': 18
    }),
    (Adjustment.WATER, {
        'name': 'Water',
        'rule_type': RULE_MISC,
        'rule_field': 'water',
        'subject_value_method': get_property_water_category,
        'comp_value_method': get_property_water_category,
        'adjustment_class': AdjustmentWater,
        'order': 17
    }),
    (Adjustment.CONDO_VIEW_FLOOR, {
        'name': 'Condo View Floor',
        'rule_type': RULE_MISC,
        'rule_field': 'condo_view_floor',
        'subject_value_method': get_condo_view_floor,
        'comp_value_method': get_condo_view_floor,
        'adjustment_class': AdjustCondoViewFloor,
        'order': 17
    })
])


def f(a, b, c):
    suma = a + b + c
    return (suma, )


if __name__ == '__main__':
    print('hello')
    z = f(2, 3, 4)
    print(z[1])
