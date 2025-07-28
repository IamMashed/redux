# helper methods for subdivision logic we apply at cma which
# defines the order of comps
from app.utils.comp_utils import get_condo_category


def equal_bedrooms(subject, comp):
    return comp.bedrooms == subject.bedrooms


def equal_subdivision(subject, comp):
    return comp.apn[:8] == subject.apn[:8]


def equal_gla_sqft(subject, comp):
    return comp.gla_sqft == subject.gla_sqft


def equal_full_baths(subject, comp):
    return comp.full_baths == subject.full_baths


def equal_half_baths(subject, comp):
    return comp.half_baths == subject.half_baths


def equal_view_condo_category(subject, comp):
    return get_condo_category(subject) == get_condo_category(comp)
