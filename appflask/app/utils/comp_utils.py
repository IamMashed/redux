from abc import ABC
from collections import Generator

from app.utils.constants import County, WHITELISTED_PROPERTY_CLASS_CODES


def water_category_index(order_list, val):
    try:
        return order_list.index(val)
    except ValueError:
        return float('inf')


def build_category_order(category):
    subject_category = category
    results = [category]
    while category and category != -1:
        category = get_next_water_category(category, subject_category)
        results.append(category)
    # replace the -1 with None
    return [x if x != -1 else None for x in results]


def get_next_water_category(category, subject_category):
    """
    subject_category: category we started at
    category: current loop category
    """
    if category == 1 and subject_category == 1:
        return 2
    if category == 2 and subject_category == 1:
        return 3
    if category == 3 and subject_category == 1:
        return 4
    if category == 4 and subject_category == 1:
        return 5
    if category == 5 and subject_category == 1:
        return -1

    if category == 2 and subject_category == 2:
        return 3
    if category == 3 and subject_category == 2:
        return 4
    if category == 4 and subject_category == 2:
        return 5
    if category == 5 and subject_category == 2:
        return -1

    if category == 3 and subject_category == 3:
        return 4
    if category == 4 and subject_category == 3:
        return 5
    if category == 5 and subject_category == 3:
        return -1

    if category == 4 and subject_category == 4:
        return 5
    if category == 5 and subject_category == 4:
        return -1

    if category == 5 and subject_category == 5:
        return 4
    if category == 4 and subject_category == 5:
        return -1

    if category == 6 and subject_category == 6:
        return None

    if not category:
        return -1


def proximity_format(query):
    with_proximity = []
    for comp in query.all():
        c = comp[0]
        c.proximity = comp[1] / 1609.0
        if c not in with_proximity:
            with_proximity.append(c)
    return with_proximity


def is_whitelisted(**data) -> bool:
    """
    Check whether property is whitelisted
    """
    whitelist = WHITELISTED_PROPERTY_CLASS_CODES[data['county']]
    if data['county'] == County.BROWARD:
        if (data['property_class'], data['property_class_type']) in whitelist or \
                (data['is_condo'] is True and data['property_class'] == 4):
            return True
    elif data['county'] in [County.MIAMIDADE, County.PALMBEACH]:
        if data['property_class'] in whitelist:
            return True
    elif data['county'] == County.NASSAU:
        if (data['property_class'], data['property_class_type']) in whitelist:
            return True
    return False


def get_whitelisted(properties):
    """
    Filter to allow only whitelisted properties.
    Whitelist is different for each county
    """
    results = []
    for property in properties:
        whitelist = WHITELISTED_PROPERTY_CLASS_CODES[property.county]
        if property.county == County.BROWARD:
            if (property.property_class, property.property_class_type) in whitelist or \
                    (property.is_condo is True and property.property_class == 4):
                results.append(property)
        elif property.county in [County.MIAMIDADE, County.PALMBEACH]:
            if property.property_class in whitelist:
                results.append(property)
        elif property.county == County.NASSAU:
            if (property.property_class, property.property_class_type) in whitelist:
                results.append(property)
        else:
            # for other counties whitelist not defined for now
            results.append(property)
    return results


class CondoCategoryIter(Generator, ABC):
    def __init__(self, current):
        self.current = current
        if current == 5:
            self.next = current - 1
        elif current == 6 or current == 0:
            self.next = None
        else:
            self.next = current + 1

    def send(self, ignored_arg):
        if (self.current == 6 or self.current == 0) and not self.next:
            self.throw()

        ret = self.current
        if self.current == 6 and self.next == 7:
            self.throw()
        if self.current == 3 and self.next == 2:
            self.throw()
        if (self.current == 5 and self.next == 4) or (self.current == 4 and self.next == 3):
            self.current, self.next = self.next, self.next - 1
            return ret
        self.current, self.next = self.next, self.next + 1
        return ret

    def throw(self, typ=None, value=None, traceback=None):
        raise StopIteration


def get_condo_category(prop):
    if prop.condo_view_influence in ['OF']:
        return 1
    elif prop.condo_view_influence in ['BF'] or (
            prop.condo_view_location == 'S' and prop.condo_view_influence == 'BF'):
        return 2
    elif prop.condo_view_influence in ['BV', 'IN']:
        return 3
    elif prop.condo_view_influence in ['LV', 'LF'] or (
            prop.condo_view_location == 'S' and prop.condo_view_influence == 'L1') or (
            prop.condo_view_location == 'S' and prop.condo_view_influence == 'L2') or (
            prop.condo_view_location == 'S' and prop.condo_view_influence == 'LF') or (
            prop.condo_view_location == 'S' and prop.condo_view_influence == 'V2'):
        return 4
    elif prop.condo_view_influence in ['GF', 'GV']:
        return 5
    # elif prop.condo_view_influence in [
    #     'PL', 'PK', 'RA', 'ST', 'CF', 'CV', 'NV', 'OL', 'FA', 'GR', 'UN'] or (
    #         prop.condo_view_location == 'S' and prop.condo_view_influence == 'CF') or (
    #         prop.condo_view_location == 'S' and prop.condo_view_influence == 'CR') or (
    #         prop.condo_view_location == 'S' and prop.condo_view_influence == 'V1'):
    #     return 6
    # return None
    else:
        return 6


def get_same_category_condos(subject, category, comps, location=False, proximity=False):
    results = []
    # category = get_condo_category(subject)
    for prop in comps:
        if prop in results:
            continue
        if proximity:
            if prop.proximity != 0:
                continue
        if location:
            if prop.condo_view_location != subject.condo_view_location:
                continue
        if category == 1 and get_condo_category(prop) == 1:
            results.append(prop)
            continue
        if category == 2 and get_condo_category(prop) == 2:
            results.append(prop)
            continue
        if category == 3 and get_condo_category(prop) == 3:
            results.append(prop)
            continue
        if category == 4 and get_condo_category(prop) == 4:
            results.append(prop)
            continue
        if category == 5 and get_condo_category(prop) == 5:
            results.append(prop)
            continue
        if category == 6 and get_condo_category(prop) == 6:
            # Modify the code so that it would always return a category 6 if
            # view_code is unknown to the system. (6 is the lowest)
            results.append(prop)
    return results


def format_comps_for_cma_log(comps):
    return [dict(id=p.id,
                 apn=p.apn,
                 address=p.address,
                 longitude=p.longitude,
                 latitude=p.latitude) for p in comps]
