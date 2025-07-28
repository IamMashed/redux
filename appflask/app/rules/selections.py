from collections import OrderedDict

RULE_SELECTION = 'selection_rules'


class Selection:
    """
    Class of selection rule names.
    Use one or few filters to construct goal query to return filtered objects
    """
    PROXIMITY_RANGE = "RANGE"
    SALE_DATE_FROM = "SALE_DATE_FROM"
    SALE_DATE_TO = "SALE_DATE_TO"
    PERCENT_GLA_LOWER = "PERCENT_GLA_LOWER"
    PERCENT_GLA_HIGHER = "PERCENT_GLA_HIGHER"
    PERCENT_LOT_SIZE_LOWER = "PERCENT_LOT_SIZE_LOWER"
    PERCENT_LOT_SIZE_HIGHER = "PERCENT_LOT_SIZE_HIGHER"
    PERCENT_SALE_LOWER = "PERCENT_SALE_LOWER"
    PERCENT_SALE_HIGHER = "PERCENT_SALE_HIGHER"
    SAME_PROPERTY_CLASS = "SAME_PROPERTY_CLASS"
    SAME_SCHOOL_DISTRICT = "SAME_SCHOOL_DISTRICT"
    SAME_TOWN = "SAME_TOWN"
    SAME_STREET = "SAME_STREET"
    SAME_PROPERTY_STYLE = "SAME_PROPERTY_STYLE"
    SAME_ONE_FAMILY_TYPES = "SAME_ONE_FAMILY_TYPES"
    SAME_AGE = "SAME_AGE"
    SAME_BUILDING = "SAME_BUILDING"
    PRIORITIZE_SAME_WATER_CATEGORIES = "PRIORITIZE_SAME_WATER_CATEGORIES"


ALL_SELECTIONS = OrderedDict([
        (Selection.PROXIMITY_RANGE,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'proximity_range',
            }),
        (Selection.SALE_DATE_FROM,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'sale_date_from',
            }),
        (Selection.SALE_DATE_TO,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'sale_date_to',
            }),
        (Selection.PERCENT_GLA_LOWER,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'percent_gla_lower',
            }),
        (Selection.PERCENT_GLA_HIGHER,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'percent_gla_higher',
            }),
        (Selection.PERCENT_LOT_SIZE_LOWER,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'percent_lot_size_lower',
            }),
        (Selection.PERCENT_LOT_SIZE_HIGHER,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'percent_lot_size_higher',
            }),
        (Selection.PERCENT_SALE_LOWER,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'percent_sale_lower',
            }),
        (Selection.PERCENT_SALE_HIGHER,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'percent_sale_higher',
            }),
        (Selection.SAME_PROPERTY_CLASS,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'same_property_class',
            }),
        (Selection.SAME_SCHOOL_DISTRICT,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'same_school_district',
            }),
        (Selection.SAME_TOWN,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'same_town',
            }),
        (Selection.SAME_STREET,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'same_street',
            }),
        (Selection.SAME_PROPERTY_STYLE,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'same_property_style',
            }),
        (Selection.SAME_ONE_FAMILY_TYPES,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'same_one_family_types',
            }),
        (Selection.SAME_AGE,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'same_age',
            }),
        (Selection.SAME_BUILDING,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'same_building',
            }),
        (Selection.PRIORITIZE_SAME_WATER_CATEGORIES,   {
            'rule_type': RULE_SELECTION,
            'rule_field': 'prioritize_same_water_categories',
            }),
        ])
