# Controller code related to the properties
# Including (not limited to):
# Finding nearby properties for comparison
# Price Adjustment to the subject property
# Price Adjustment of the subject property
import logging
from collections import OrderedDict
from datetime import datetime
from typing import Union

# import time
from geoalchemy2 import Geography
from sqlalchemy import and_, or_, func, cast
from sqlalchemy.orm import contains_eager

from app.controller.subdivision_logic import (equal_bedrooms,
                                              equal_full_baths,
                                              equal_half_baths,
                                              equal_view_condo_category,
                                              equal_subdivision,
                                              equal_gla_sqft)
from app.database.models import Sale, Assessment
from app.database.models.property import Property, CmaNotification
from app.routing.services import PropertyService, ReportService
from app.rules import exceptions
from app.rules.adjustments import Adjustment
from app.rules.controllers import RulesController
from app.rules.models import PropertiesRules, ALL_ADJUSTMENTS
from app.rules.selections import Selection
from app.settings.models import AssessmentDate, Ratio
from app.utils.comp_utils import (get_next_water_category,
                                  get_whitelisted,
                                  CondoCategoryIter,
                                  get_condo_category,
                                  get_same_category_condos,
                                  format_comps_for_cma_log,
                                  build_category_order,
                                  water_category_index)
from app.utils.constants import County


class FilterName:
    SALE_DATE_RANGE = "SALE_DATE_RANGE"
    SALE_NOT_QUALIFIED = "NOT_QUALIFIED_SALE"
    SAME_SECTION_BLOCK_OR_STREET = "SAME_SECTION_BLOCK_OR_STREET"
    CORRECT_ASSESSMENT = "CORRECT_ASSESSMENT"
    SUBJECT_AS_COMP = 'SUBJECT_AS_COMP'
    CONDO_LOGIC = 'CONDO_LOGIC'
    # SUBJECT_AGE = 'SUBJECT_AGE'


class CMAQueryFilter:
    def __init__(self, subject, rules_controller, names=None, is_compute_log=False, **kwargs):
        """
        Initialize CMA query filter
        :param subject: The Subject property
        :param rules_controller: The rules controller
        :param names: A list of filter names
        """
        self._subject = subject
        self._rules_controller = rules_controller

        self._params = kwargs
        self._names = names or []
        self.cma_log = OrderedDict()
        self._is_compute_log = is_compute_log
        self.mass_cma = kwargs.get('mass_cma', None)

    @property
    def is_compute_log(self):
        return self._is_compute_log

    def filter_all(self, query, exclude=None):
        """
        Apply all query filters
        """
        if exclude is None:
            exclude = ()

        if query is None:
            raise ValueError('Invalid query object')

        approved_comps = None
        for name in self._names:
            if name in exclude:
                continue
            query, approved_comps = self.filter(query, name, approved_comps)

        return query

    def filter(self, query, filter_name, before_comps=None):
        """
        Property query filter

        :param query: The query object
        :param filter_name: The name of the filter
        :param before_comps
        """
        # get filter method by name
        # import time
        filter_method = self._get_filter_method(filter_name)
        next_query, enabled = filter_method(query)
        after_comps = None

        if self.is_compute_log:
            if not self.mass_cma and filter_name != Selection.PROXIMITY_RANGE \
                    and filter_name != FilterName.CORRECT_ASSESSMENT:
                # start_time = time.time()
                if not before_comps:
                    before_count = query.distinct().count()
                else:
                    before_count = len(before_comps)

                after_count = next_query.distinct().count()

                difference = before_count - after_count
                filtered_comps = []
                if difference > 0:
                    # print(f'computing diff...')
                    if not before_comps:
                        before_comps = query.with_entities(Property.id,
                                                           Property.apn,
                                                           Property.latitude,
                                                           Property.longitude,
                                                           Property.address).all()
                        before_comps = set(before_comps)
                    after_comps = next_query.with_entities(Property.id,
                                                           Property.apn,
                                                           Property.latitude,
                                                           Property.longitude,
                                                           Property.address).all()
                    after_comps = set(after_comps)
                    filtered_comps = before_comps.difference(after_comps)
                    filtered_comps = [dict(id=c[0],
                                           apn=c[1],
                                           longitude=c[3],
                                           latitude=c[2],
                                           address=c[4]) for c in filtered_comps]
                elif difference == 0:
                    after_comps = before_comps
                # end_time = time.time()
                # diff = (end_time - start_time)
                # print(f'time at filter {filter_name} ... {diff}')

                self.cma_log[filter_name] = dict(
                    enabled=enabled,
                    before_count=before_count,
                    removed=before_count - after_count,
                    filtered_comps=filtered_comps)
        return next_query, after_comps

    def has_joined_entity(self, query, entity):
        """
        Check whether query has joined entity
        :param query: The query object
        :param entity: The entity class
        """
        if entity in [mapper.entity for mapper in query._join_entities]:
            return True
        return False

    def _join_table(self, query, entity_model, entity_location):
        if self.has_joined_entity(query, entity_model):
            return query

        if query._primary_entity:
            query = query.join(entity_location).options(contains_eager(entity_location))
        else:
            # Expression based (no primary entity, cannot specify load behaviour
            query = query.join(entity_location)

        return query

    def _get_filter_method(self, filter_name: str):
        """
        Factory method to get filter method by filter name
        """
        # selection filters
        if filter_name == Selection.PROXIMITY_RANGE:
            return self._proximity_range_filter
        if filter_name == Selection.SAME_BUILDING:
            return self._same_building_filter
        if filter_name == Selection.PERCENT_SALE_LOWER:
            return self._percent_sale_price_lower_filter
        if filter_name == Selection.PERCENT_SALE_HIGHER:
            return self._percent_sale_price_higher_filter
        elif filter_name == Selection.PERCENT_GLA_LOWER:
            return self._percent_gla_lower_filter
        elif filter_name == Selection.PERCENT_GLA_HIGHER:
            return self._percent_gla_higher_filter
        elif filter_name == Selection.PERCENT_LOT_SIZE_HIGHER:
            return self._percent_lot_size_higher_filter
        elif filter_name == Selection.PERCENT_LOT_SIZE_LOWER:
            return self._percent_lot_size_lower_filter
        elif filter_name == Selection.SAME_ONE_FAMILY_TYPES:
            return self._same_one_family_types_filter
        elif filter_name == Selection.SAME_PROPERTY_CLASS:
            return self._same_property_class_filter
        elif filter_name == Selection.SAME_PROPERTY_STYLE:
            return self._same_property_style_filter
        elif filter_name == Selection.SAME_SCHOOL_DISTRICT:
            return self._same_school_district_filter
        elif filter_name == Selection.SAME_STREET:
            return self._same_street_filter
        elif filter_name == Selection.SAME_TOWN:
            return self._same_town_filter

        # additional filters
        elif filter_name == FilterName.SALE_DATE_RANGE:
            return self._sale_date_range_filter
        elif filter_name == FilterName.SALE_NOT_QUALIFIED:
            return self._sale_not_qualified
        elif filter_name == FilterName.SAME_SECTION_BLOCK_OR_STREET:
            return self._same_block_section_or_street_filter
        elif filter_name == FilterName.CORRECT_ASSESSMENT:
            return self._correct_assessment_filter
        # elif filter_name == FilterName.SUBJECT_AS_COMP:
        #     return self._subject_as_comp_filter
        # elif filter_name == FilterName.SUBJECT_AGE:
        #     return self._subject_age
        else:
            raise ValueError(filter_name)

    def _proximity_range_filter(self, query):
        """
        Subject proximity range query filter
        """
        enabled = True  # this filter is always enabled
        meters = self._rules_controller.get_proximity_in_meters()

        # https://gis.stackexchange.com/questions/247113/how-to-properly-set-up-indexes-for-postgis-distance-queries/247131
        query = query.add_column(func.ST_DistanceSphere(
            Property.geo, self._subject.geo).label('proximity')).filter(
            func.ST_DWithin(
                cast(Property.geo, Geography(geometry_type=None)),
                cast(self._subject.geo, Geography(geometry_type=None)),
                meters)
        ).order_by(
            func.ST_DistanceSphere(
                Property.geo, self._subject.geo), Property.apn
        )
        return query, enabled

    def _same_building_filter(self, query):
        enabled = False
        if self._subject.is_condo and self._rules_controller.get_value(Selection.SAME_BUILDING):
            meters = 0
            query = query.filter(
                func.ST_DWithin(
                    cast(Property.geo, Geography(geometry_type=None)),
                    cast(self._subject.geo, Geography(geometry_type=None)),
                    meters)
            ).order_by(
                func.ST_DistanceSphere(
                    Property.geo, self._subject.geo)
            )
            enabled = True
        return query, enabled

    def _percent_gla_higher_filter(self, query):
        """
        Percent GLA higher query filter
        """
        enabled = False
        percent_gla_higher = self._rules_controller.get_value(Selection.PERCENT_GLA_HIGHER)
        if percent_gla_higher and self._subject.gla_sqft:
            query = query.filter(or_(Property.gla_sqft <= self._subject.gla_sqft *
                                     (1.0 + percent_gla_higher / 100.0), Property.gla_sqft is None))
            enabled = True
        return query, enabled

    def _percent_gla_lower_filter(self, query):
        """
        Percent GLA lower query filter
        """
        enabled = False
        percent_gla_lower = self._rules_controller.get_value(Selection.PERCENT_GLA_LOWER)
        if percent_gla_lower and self._subject.gla_sqft:
            query = query.filter(or_(Property.gla_sqft >= self._subject.gla_sqft *
                                     (1.0 - percent_gla_lower / 100.0), Property.gla_sqft is None))
            enabled = True
        return query, enabled

    def _percent_lot_size_higher_filter(self, query):
        """
        Percent Lot Size higher query filter
        """
        enabled = False
        percent_lot_size_higher = self._rules_controller.get_value(Selection.PERCENT_LOT_SIZE_HIGHER)
        if percent_lot_size_higher and self._subject.lot_size:
            query = query.filter(or_(Property.lot_size <= self._subject.lot_size *
                                     (1.0 + percent_lot_size_higher / 100.0), Property.lot_size is None))
            enabled = True
        return query, enabled

    def _percent_lot_size_lower_filter(self, query):
        """
        Percent Lot Size lower query filter
        """
        enabled = False
        percent_lot_size_lower = self._rules_controller.get_value(Selection.PERCENT_LOT_SIZE_LOWER)
        if percent_lot_size_lower and self._subject.lot_size:
            query = query.filter(or_(Property.lot_size >= self._subject.lot_size *
                                     (1.0 - percent_lot_size_lower / 100.0), Property.lot_size is None))
            enabled = True
        return query, enabled

    def _percent_sale_price_lower_filter(self, query):
        """
        Percent sale price lower range query filter
        """
        enabled = False
        current_market_value = self._params.get('current_market_value', None)

        min_value = 0
        percent_sale_lower = self._rules_controller.get_value(Selection.PERCENT_SALE_LOWER)
        if percent_sale_lower:
            min_value = int(current_market_value * (1.0 - percent_sale_lower / 100.0))
            enabled = True

        query = self._join_table(query, Sale, Property.sales)
        query = query.filter(
            Sale.price >= min_value
        )

        return query, enabled

    def _percent_sale_price_higher_filter(self, query):
        """
        Percent sale price higher range query filter
        """
        enabled = False
        current_market_value = self._params.get('current_market_value', None)

        max_value = 1000000000  # Assumed maximum
        percent_sale_higher = self._rules_controller.get_value(Selection.PERCENT_SALE_HIGHER)
        if percent_sale_higher:
            max_value = int(current_market_value * (1.0 + percent_sale_higher / 100.0))
            enabled = True

        query = self._join_table(query, Sale, Property.sales)
        query = query.filter(
            Sale.price <= max_value
        )
        return query, enabled

    def _same_one_family_types_filter(self, query):
        """
        Same family types query filter
        """
        enabled = False
        # TODO: same one family types. For now only for Nassau
        if self._rules_controller.get_value(Selection.SAME_ONE_FAMILY_TYPES) and self._subject.property_class:
            if self._subject.county == County.NASSAU:
                first_digit = str(self._subject.property_class)[:1]
                if first_digit == '2':
                    query = query.filter(Property.property_class >= 2000, Property.property_class <= 2999)
                    enabled = True
        return query, enabled

    def _same_property_class_filter(self, query):
        """
        Same property class query filter
        """
        enabled = False
        if self._rules_controller.get_value(Selection.SAME_PROPERTY_CLASS) and self._subject.property_class:
            enabled = True
            if self._subject.county == County.NASSAU:
                last_ignored = self._subject.property_class // 10
                upper_limit = (last_ignored + 1) * 10
                lower_limit = last_ignored * 10
                query = query.filter(Property.property_class >= lower_limit, Property.property_class < upper_limit)
            else:
                query = query.filter(Property.property_class == self._subject.property_class)
        return query, enabled

    def _same_property_style_filter(self, query):
        """
        Same property style query filter
        """
        enabled = False
        if self._rules_controller.get_value(Selection.SAME_PROPERTY_STYLE) and self._subject.property_style:
            query = query.filter(Property.property_style == self._subject.property_style)
            enabled = True
        return query, enabled

    def _same_school_district_filter(self, query):
        """
        Same school district query filter
        """
        enabled = False
        if self._rules_controller.get_value(Selection.SAME_SCHOOL_DISTRICT) and self._subject.school_district:
            query = query.filter(Property.school_district == self._subject.school_district)
            enabled = True
        return query, enabled

    def _same_street_filter(self, query):
        """
        Sam property street query filter
        """
        enabled = False
        if self._rules_controller.get_value(Selection.SAME_STREET) and self._subject.street:
            query = query.filter(Property.street == self._subject.street)
            enabled = True
        return query, enabled

    def _same_town_filter(self, query):
        """
        Same property town query filter
        """
        enabled = False
        if self._rules_controller.get_value(Selection.SAME_TOWN) and self._subject.town:
            query = query.filter(Property.town == self._subject.town)
            enabled = True
        return query, enabled

    def _sale_date_range_filter(self, query):
        """
        Subject sales date range query filter
        """
        enabled = False
        sale_dates_from = self._params.get('sale_dates_from', None)
        sale_dates_to = self._params.get('sale_dates_to', None)
        min_date_default, max_date_default, enabled = self._rules_controller.get_date_range()

        if sale_dates_from and sale_dates_to:
            # get the sales date range from the selection rules table
            enabled = True
            min_date = sale_dates_from or min_date_default
            max_date = sale_dates_to or max_date_default
        else:
            min_date, max_date = min_date_default, max_date_default

        query = self._join_table(query, Sale, Property.sales)
        # arms_length is not False & 'date' in sale date range
        query = query.filter(
            and_(
                Sale.date >= min_date,
                Sale.date <= max_date,
            )
        )
        return query, enabled

    def _sale_not_qualified(self, query):
        enabled = True
        query = query.filter(~Sale.arms_length.is_(False))
        return query, enabled

    def _same_block_section_or_street_filter(self, query):
        """
        Subject same block & section or same street query filter
        """
        enabled = True
        query = query.filter(
            or_(
                and_(
                    Property.block == self._subject.block,
                    Property.section == self._subject.section
                ),
                Property.street == self._subject.street
            )
        )
        return query, enabled

    def _correct_assessment_filter(self, query):
        """
        Correct assessment filter
        """
        enabled = True
        assessment_date = self._params.get('assessment_date', None)

        # join with correct property assessments since we may have
        # more than one assessment per property
        if assessment_date is None:
            # pick the latest assessment by valuation date
            enabled = False
            assessment_date = AssessmentDate.query.filter_by(
                county=self._subject.county
            ).order_by(AssessmentDate.valuation_date.desc()).first()

        query = self._join_table(query, Assessment, Property.assessments)
        query = query.filter(Assessment.assessment_id == assessment_date.id)

        return query, enabled

    # def _subject_as_comp_filter(self, query):
    #     """
    #     Included subject as first comparable under certain conditions
    #     """
    #     enabled = True
    #     rule = self._rules_controller.rules
    #     if rule.subject_sales_from and self._subject.last_sale:
    #         if rule.subject_sales_from > self._subject.last_sale.date:
    #             query = query.filter(Property.id != self._subject.id)
    #             enabled = False
    #     return query, enabled

    # def _subject_age(self, query):
    #     """
    #     For properties which are new, only use comps with age less than 15 years old.
    #     """
    #     # if property age null do not filter
    #     enabled = True
    #     if not self._rules_controller.get_value(Selection.SAME_AGE) or not self._subject.age:
    #         enabled = False
    #         return query, enabled
    #     current_year = datetime.now().year
    #     if self._subject.age and self._subject.age >= current_year - 10:
    #         query = query.filter(Property.age > current_year - 15)
    #     return query, enabled


class CompsStatus:
    GOOD = "good"
    BAD = "bad"
    FAIL = "fail"


class SingleCmaController(object):
    """
    Main Business Logic on doing the CMA Analysis of any property.

    A flow of operation:
    - Load / Set rules that are best applicable for the given area
    - Find comparables
    - Calculate the results we require, that can be:
       Our Assessment, Break down of adjustments for comps,
       a list of 1-X good, bad, or mixed comps.
    """
    _good_comps = None
    _bad_comps = None
    _good_bad_comps = None
    _all_comps = None
    _failed_comps = None

    properties_rules = None
    rules_controller = None
    subject_assessment = None
    assessment_ratio = None
    assessment_date = None
    current_market_value = None
    sale_dates_from = None
    sale_dates_to = None
    query_filter = None
    assessment_value = None
    delta = None  # https://app.asana.com/0/1147405519499344/1183136849587487

    DEFAULT_COMPS_AMOUNT = 4
    REQUIRED_COMPS_AMOUNT = 0

    def __init__(self, subject, subject_assessment=None, properties_rules=None,
                 assessment_ratio=None, mass_cma=False,
                 app=None, assessment_date=None, sale_dates_from=None,
                 sale_dates_to=None, rules_controller=None, is_compute_log=False
                 ):
        if assessment_date and subject_assessment:
            print("Warning: It is not correct to specify 'assessment_date' and 'subject_assessment' at the same time")

        self._is_compute_log = is_compute_log
        self._all_comps = []
        self.subject_property = subject
        self.subject_sale_price = self.subject_property.last_sale.price if self.subject_property.last_sale else None

        self.app = app
        self.mass_cma = mass_cma
        self.assessment_date = assessment_date

        # get or load from database subject assessment
        self.subject_assessment = subject_assessment or self.load_subject_assessment()

        # if still no assessment, raise exception since CMA can not run without assessment object
        if not self.subject_assessment or not self.subject_assessment.assessed_value:
            raise exceptions.AssessmentException('No Subject assessment or a zero value')

        # get or load from database assessment ratio
        self.assessment_ratio = assessment_ratio or self.load_assessment_ratio()

        # get correct subject assessment value: override_value if exists or assessment_value
        self.assessment_value = self.subject_assessment.assessed_value

        # extend subject with 'assessment_value' & 'market_value' to reduce amount of db queries
        self.subject_property.assessment_value = self.assessment_value

        # calculate market value based on assessed_value ('assessment_value' or 'override_value') value and ratio
        # 'market_value' formula : assessed_value/ratio
        # for the Florida counties market value will be the same as assessment value since ratio = 1
        self.subject_property.market_value = self.get_market_value(self.assessment_value, self.assessment_ratio)

        # get of load properties rules, used for CMA calculations
        self.properties_rules = properties_rules or self.load_properties_rules()
        self.rules_controller = rules_controller or self.get_rules_controller(properties_rules)

        self.sale_dates_from = sale_dates_from
        self.sale_dates_to = sale_dates_to

        # calculate subject market delta
        # note, that delta calculation must be called after subject market value and rules_controller are calculated
        self.delta = self.get_subject_market_delta()

        # Verify no violations
        if mass_cma:
            for rule in self.rules_controller.get_required_adjustments():
                adjustment_info = ALL_ADJUSTMENTS[rule]
                if rule != Adjustment.TIME:
                    value = getattr(subject, adjustment_info['property_field'])
                    if not value:
                        raise exceptions.SubjectLacksDataException("Subject violates Mass CMA requirements")

    def is_sale_within_date_range(self, sale):
        """
        Check whether sale is within date range
        """
        sale_dates_from = self.sale_dates_from or self.rules_controller.get_value('SALE_DATE_FROM')
        sale_dates_to = self.sale_dates_to or self.rules_controller.get_value('SALE_DATE_TO')

        if sale and sale_dates_from and sale_dates_to:
            # sale within date range
            if sale_dates_from <= sale.date <= sale_dates_to:
                return True

        return False

    def is_sale_after_date_range(self, sale):
        """
        Check whether sale is after date range
        """
        sale_dates_to = self.sale_dates_to or self.rules_controller.get_value('SALE_DATE_TO')

        if sale and sale_dates_to:
            # sale within date range
            if sale.date > sale_dates_to:
                return True
        return False

    def sold_after_date_range_higher_assessment_alert(self):
        """
        Create alert notification for subject sold for higher than assessed value after sale date range
        """
        sale = self.subject_property.last_sale
        if not sale:
            logging.warning("No subject last sale")
            return

        price = sale.price
        assessed_value = self.subject_property.assessment_value

        # sale after date range & subj sale is higher than assessed value
        notification = None
        if self.is_sale_after_date_range(sale) and price > assessed_value:
            formatted_price = ReportService.format_price(price)
            notification = CmaNotification(
                status='error',
                message=f'Subj sold for higher ({formatted_price}) than the assessed value after the Sale Date Range'
            )

        if notification:
            self.subject_property.cma_notification = notification

    def sold_withing_date_range_disqualified_sale_alert(self):
        """
        Create cma notification alert object if:
            - subject sold in a disqualified sale.
            - sale within sale date range
        """
        sale = self.subject_property.last_any_sale

        if not sale:
            logging.warning("No subject last sale")
            return
        price = sale.price
        date = sale.date

        # sale within date range & subj sale disqualified
        notification = None
        if self.is_sale_within_date_range(sale) and self.subject_property.is_disqualified:
            formatted_price = ReportService.format_price(price)
            formatted_date = ReportService.format_date(date)

            notification = CmaNotification(
                status='error',
                message=f'Note: Subject Disqualified Sale on {formatted_date} for {formatted_price}.'
            )

        if notification:
            self.subject_property.cma_notification = notification

    def passed_subject_sale_rule(self):
        """
        If the subject is a "Subject Sale" (meaning, if the property was sold within the SALE_DATE_RANGE filter:

        Calculate the DELTA as:
        Delta = Current Assessment - (Sale Price - Cost of Sale)

        If it is Nassau/Suffolk then do not do the "- Cost of Sale" part

        If Delta <= 0 it means this is a bad case.
        If Delta > 0 then this is a good case

        Bad Case:
        - Single CMA. Display the Banner as we were supposed in this task: Subject Sale Date Range action
        - Mass CMA. set subject_sale column = Delta. Reject the Good/All averages computation,
        it is not important. Saving column = Delta

        Good Case:
        - Single CMA. Display a Green banner saying "Good Subject Sale Property"
        - Mass CMA. set subject_sale column = Delta. Reject the Good/All averages computation,
        it is not important. Saving column = Delta
        """
        subject_sale = self.subject_property.last_sale
        arms_length = subject_sale.arms_length if subject_sale else None
        if self.is_sale_within_date_range(subject_sale) and arms_length:
            if self.mass_cma:
                return False  # sale date within range means function not passing. Used for mass cma

            cma_status = self.delta > 0
            self.subject_property.cma_notification = self.get_cma_notification(cma_status=cma_status)

            return cma_status

        return True  # rules not set

    def get_subject_cos(self):
        """
        Get subject cost of sale value
        There is a default county specific `cost_of_sale` configuration:
            - Miamidade - 15%
            - Broward - 10%
        For others return `cost_of_sale = 0`
        """
        subject_sale = self.subject_property.last_sale
        cos_value = 0

        if self.subject_property.county in County.get_florida_counties():
            cos_value = subject_sale.price * (self.properties_rules.cost_of_sale or 0) / 100

        return cos_value

    def get_subject_market_delta(self):
        """
        Get subject market delta.
        Calculation Formulas:
            1. 'subject market delta' = 'market value' - 'adjusted sale price'
            2. 'adjusted sale price' = 'last sale price' - `get_subject_cos()`

        """
        subject_sale = self.subject_property.last_sale
        cost_of_sale = self.get_subject_cos()

        # calculate the 'subject market delta': 'market value' - 'adjusted sale price'
        # 'adjusted sale price' = 'last sale price' - 'get_subject_cos()'
        market_delta = self.subject_property.market_value - (subject_sale.price - cost_of_sale)

        return market_delta

    def subject_as_comp(self, comps):
        initial_comps = comps
        filtered_comps = []
        enabled = False
        before_count = len(comps)

        # get subject sale date
        last_sale_date = None
        last_sale = self.subject_property.last_sale
        if last_sale:
            last_sale_date = last_sale.date

        # get range of sale dates from rules
        from_date, to_date, enabled = self.rules_controller.get_date_range()

        # check whether subject sale date in range
        if from_date and to_date and last_sale_date:
            if from_date <= last_sale_date <= to_date:
                subject_as_comp = self.subject_property
                subject_as_comp.proximity = 0
                comps.insert(0, subject_as_comp)
                enabled = True

            filtered_comps = [c for c in initial_comps if c not in comps]
            filtered_comps = format_comps_for_cma_log(filtered_comps)

        if self._is_compute_log:
            self.query_filter.cma_log[FilterName.SUBJECT_AS_COMP] = dict(
                enabled=enabled,
                before_count=before_count,
                removed=len(filtered_comps),
                filtered_comps=filtered_comps,
            )
        return comps

    def subject_age_filter(self, comps):
        initial_comps = comps
        enabled = False
        filtered_comps = []
        before_count = len(comps)
        current_year = datetime.now().year

        if self.rules_controller.get_value(Selection.SAME_AGE) and \
                self.subject_property.age and \
                self.subject_property.age >= current_year - 10:
            enabled = True
            comps = [c for c in initial_comps if c.age > current_year - 15]
            older_comps = [c for c in initial_comps if c.age <= current_year - 15]

            # If not enough comps, only then seek for more comps outside of the years restriction
            if len(comps) < 12:
                comps += older_comps[:(12 - len(comps))]

            filtered_comps = [c for c in initial_comps if c not in comps]
            filtered_comps = format_comps_for_cma_log(filtered_comps)

        if self._is_compute_log:
            self.query_filter.cma_log[Selection.SAME_AGE] = dict(
                enabled=enabled,
                before_count=before_count,
                removed=len(filtered_comps),
                filtered_comps=filtered_comps,
                # this one has passed comps since it is the last filter being applied
                passed_comps=format_comps_for_cma_log(comps)
            )
        return comps

    def prioritize_same_water_categories(self, comps):
        """
        Another some kind of a filter for comparables. The reason we are not using database query is
        because we may need to add another categories if we are missing required amount of 12 comps.
        That is why we bring all from database and do rest filtering in python code.
        """
        # filtered_comps = []
        # added_from_next_category_comps = []
        # water_categories_enabled = False
        # before_count = len(comps)
        # if self.rules_controller.get_value(Selection.PRIORITIZE_SAME_WATER_CATEGORIES):
        #     aggregated_comps, added_from_next_category_comps = self.get_waterfront_comps(comps)
        #     water_categories_enabled = True
        #     filtered_comps = [x for x in comps if x not in aggregated_comps]
        #     filtered_comps = format_comps_for_cma_log(filtered_comps)
        #     added_from_next_category_comps = format_comps_for_cma_log(added_from_next_category_comps)
        #     comps = aggregated_comps
        # self.query_filter.cma_log[Selection.PRIORITIZE_SAME_WATER_CATEGORIES] = dict(
        #     enabled=water_categories_enabled,
        #     before_count=before_count,
        #     removed=len(filtered_comps),
        #     filtered_comps=filtered_comps,
        #     added_from_next_category_comps=added_from_next_category_comps,
        #     added_count=len(added_from_next_category_comps),
        # )
        # self.query_filter.log.append(f'query count {before_count} before
        # {Selection.PRIORITIZE_SAME_WATER_CATEGORIES}')
        # return comps

        if self.rules_controller.get_value(Selection.PRIORITIZE_SAME_WATER_CATEGORIES):
            category_order = build_category_order(self.subject_property.water_category)
            comps = sorted(comps,
                           key=lambda c: water_category_index(category_order,
                                                              c.water_category))
        return comps

    def apply_condo_logic(self, comps):
        """
        When picking the comps for condos:
        if the view is not in Category 1-5 - do not go to other categories. Any location code is allowed
        If less than 12 comps in the building - look for the nearby buildings.
        Should work as it is now really, just don't go to other categories

        If View is in Category 1 to 5 then:
        Find comps within the same building. If less than 12, then do next until 12 is reached:
        1. Search for comps within the same building
        2. go to other buildings
        3. then loosen location code
        4. switch to a lower category type (5 is final), tighten the location code. Go to step 1

        If we start with Category 5, then we can loosen to Category 4. Cannot go to Cat 3,2,1.
        """

        if self.subject_property.county != County.MIAMIDADE:
            return comps

        initial_comps = comps
        # before_count = len(comps)
        result_comps = []
        # added_from_next_category_comps = []
        # enabled = False

        if not self.subject_property.condo_view_influence:
            result_comps = comps

        elif self.subject_property.county == County.MIAMIDADE:
            subject_condo_category = get_condo_category(self.subject_property)
            comps_with_condo_view_location = [c for c in initial_comps if c.condo_view_location]
            # enabled = True

            # TODO: what if subject condo category is None
            # aggregate all category and get difference from initial comps
            # if not subject_condo_category:
            #     condos_with_category = []
            #     for cat in range(1, 7):
            #         condos_with_category += get_same_category_condos(self.subject_property, cat,
            #                                                          comps_with_condo_view_location)
            #         result_comps = [c for c in initial_comps if c not in condos_with_category]
            # return result_comps

            if subject_condo_category == 6 or not subject_condo_category:
                result_comps = get_same_category_condos(self.subject_property, 6,
                                                        comps_with_condo_view_location)
                # return result_comps
            else:
                c_iter = CondoCategoryIter(subject_condo_category)
                for category in c_iter:
                    # try same location and same category and same building
                    s_comps = get_same_category_condos(self.subject_property, category,
                                                       comps_with_condo_view_location,
                                                       location=True,
                                                       proximity=True,
                                                       )
                    f_comps = [c for c in s_comps if c not in result_comps]
                    result_comps += f_comps
                    if len(result_comps) >= 12:
                        break

                    # go to next building
                    s_comps = get_same_category_condos(self.subject_property, category,
                                                       comps_with_condo_view_location,
                                                       location=True,
                                                       proximity=False,
                                                       )
                    f_comps = [c for c in s_comps if c not in result_comps]
                    result_comps += f_comps
                    if len(result_comps) >= 12:
                        break

                    # loosen location
                    s_comps = get_same_category_condos(self.subject_property, category,
                                                       comps_with_condo_view_location,
                                                       location=False,
                                                       proximity=False,
                                                       )
                    f_comps = [c for c in s_comps if c not in result_comps]
                    result_comps += f_comps
                    if len(result_comps) >= 12:
                        break
        else:
            result_comps = initial_comps

        # if self._is_compute_log:
        #     filtered_comps = [c for c in initial_comps if c not in result_comps]
        #     filtered_comps = format_comps_for_cma_log(filtered_comps)
        #     self.query_filter.cma_log[FilterName.CONDO_LOGIC] = dict(
        #         enabled=enabled,
        #         before_count=before_count,
        #         removed=len(filtered_comps),
        #         filtered_comps=filtered_comps,
        #     )
        if len(result_comps) < len(initial_comps):
            filtered_comps = [c for c in initial_comps if c not in result_comps]
            result_comps += filtered_comps

        return result_comps

    def get_cma_notification(self, cma_status):
        """
        Status of subject sale rules. Good or Bad.
        """
        if self.delta is None:
            return None

        market_value = self.subject_property.market_value
        sale = self.subject_property.last_sale.price
        cost_of_sale = self.get_subject_cos()

        raw = '${:,.0f}'
        difference = f"Difference - {raw.format(self.delta)}"

        # prepare parts of display text
        current_text = f"Current - {raw.format(market_value)}"
        sale_text = f"Sale - {raw.format(sale)}"
        cost_of_sale_text = f"Cost of Sale - {raw.format(cost_of_sale)}"

        if cost_of_sale == 0:
            text = f"{current_text}, {sale_text}."
        else:
            text = f"{current_text}, {sale_text}, {cost_of_sale_text}."

        if cma_status:
            return CmaNotification(status='success', message=f'Good Subject Sale. {difference} {text}')
        else:
            return CmaNotification(status='error', message=f'Bad Subject Sale. {difference} {text}')

    def get_rules_controller(self, properties_rules=None):
        """
        Get rules controller
        :param properties_rules: The properties rules object
        """
        rules_controller = RulesController(
            properties_rules or self.load_properties_rules(),
            valuation_date=self.subject_assessment.assessment_date.valuation_date
        )
        return rules_controller

    def load_subject_assessment(self):
        """
        Load subject assessment from database
        """
        if self.assessment_date:
            assessments = self.subject_property.assessments
            found = [a for a in assessments if a.assessment_id == self.assessment_date.id]
            # if we found more than one assessment it means something is wrong in database
            # there should be only one assessment for each assessment_date
            if not found:
                raise exceptions.SubjectLacksDataException('Subject lacks assessment')
            if len(found) > 1:
                raise exceptions.SubjectLacksDataException(
                    'Subject got multiple assessments. '
                    'Something was incorrectly inserted into database'
                )
            return found[0]
        else:
            # if no assessment no ratio no assessment_date supplied
            subject_assessment = PropertyService.get_property_last_assessment(self.subject_property.id)
            self.assessment_date = subject_assessment.assessment_date

            return subject_assessment

    def get_market_value(self, assessment_value, ratio_value) -> Union[int, None]:
        """
        Get property market value
        """
        if assessment_value:
            return int(assessment_value / ratio_value)
        return None

    def load_assessment_ratio(self):
        """
        Load assessment ratio from database
        """
        # this case is for single cma. At api stage we make sure
        # we get the latest assessment with property
        if self.assessment_date and self.assessment_date.tax_year:
            tax_year = self.assessment_date.tax_year
        else:
            tax_year = self.subject_assessment.assessment_date.tax_year

        return Ratio.get_ratio(tax_year, self.subject_property.county, self.subject_property.town)

    def load_properties_rules(self):
        """
        Load properties rules from database
        """
        # Load the required rules for the property analysis from the database

        county = self.subject_property.county
        town = self.subject_property.town

        if self.assessment_date:
            year = self.assessment_date.tax_year
        elif self.subject_assessment:
            year = self.subject_assessment.assessment_date.tax_year
        else:
            year = None

        return PropertiesRules.load_rules(county, town, year=year)

    def _get_base_comps_query(self):
        # create query to filter objects by county
        query = PropertyService.get_property_query(
            mass_cma=self.mass_cma,
            county=self.subject_property.county)

        # drop subject from property. Later we will add if it passes subject as a comp condition.
        query = query.filter(Property.id != self.subject_property.id)

        # compare condo to condo, house to house
        if self.subject_property.is_condo:
            query = query.filter(Property.is_condo.is_(True))
        else:
            query = query.filter(Property.is_condo.isnot(True))
        return query

    def _get_nearby_comps_query(self, limit_count=10):
        """
        Get nearby comparatives query
        """
        query = self._get_base_comps_query()

        # declare filter names to get nearby comparatives
        filter_names = [
            Selection.PROXIMITY_RANGE,
            FilterName.SAME_SECTION_BLOCK_OR_STREET,
            FilterName.SALE_DATE_RANGE,
            FilterName.SALE_NOT_QUALIFIED
        ]

        # create CMA query filter
        self.query_filter = CMAQueryFilter(subject=self.subject_property,
                                           rules_controller=self.rules_controller,
                                           names=filter_names,
                                           mass_cma=self.mass_cma,
                                           is_compute_log=self._is_compute_log
                                           )
        query = self.query_filter.filter_all(query)
        print(query)
        # limit output with 'limit_count' value
        query = query.limit(limit_count)

        return query

    def _get_suitable_comps_query(self):
        """
        Get query to fetch suitable comparatives
        """
        query = self._get_base_comps_query()

        if not self.rules_controller.get_value(Selection.PROXIMITY_RANGE):
            raise exceptions.SubjectLacksDataException('Rules controller missing proximity range information')

        # declare filter names
        filter_names = [
            Selection.PROXIMITY_RANGE,
            FilterName.SALE_DATE_RANGE,
            FilterName.SALE_NOT_QUALIFIED,
            Selection.PERCENT_SALE_LOWER,
            Selection.PERCENT_SALE_HIGHER,
            Selection.PERCENT_GLA_LOWER,
            Selection.PERCENT_GLA_HIGHER,
            Selection.PERCENT_LOT_SIZE_LOWER,
            Selection.PERCENT_LOT_SIZE_HIGHER,
            Selection.SAME_ONE_FAMILY_TYPES,
            Selection.SAME_PROPERTY_CLASS,
            Selection.SAME_SCHOOL_DISTRICT,
            Selection.SAME_TOWN,
            Selection.SAME_STREET,
            Selection.SAME_PROPERTY_STYLE,
            FilterName.CORRECT_ASSESSMENT,
            # FilterName.SUBJECT_AS_COMP,
            # FilterName.SUBJECT_AGE,
            Selection.SAME_BUILDING,
        ]

        # query params
        params = {
            'sale_dates_from': self.sale_dates_from,
            'sale_dates_to': self.sale_dates_to,
            'current_market_value': self.subject_property.market_value,
            'assessment_date': self.assessment_date
        }

        # create query filter and apply all declared filter names
        self.query_filter = CMAQueryFilter(subject=self.subject_property,
                                           rules_controller=self.rules_controller,
                                           names=filter_names,
                                           mass_cma=self.mass_cma,
                                           is_compute_log=self._is_compute_log,
                                           **params)
        filters_query = self.query_filter.filter_all(query)

        return filters_query

    # @timeit
    def get_suitable_comps(self):
        comps = self._get_suitable_comps_query().all()

        # raise and proceed masscma if subject prop does not have enough comps
        if len(comps) < 2 and self.mass_cma:
            raise exceptions.NotEnoughCompsException(f'Property {self.subject_property.id} lacks comparables')

        # show banner when zero comps
        if len(comps) == 0 and not self.mass_cma:
            self.subject_property.cma_notification = CmaNotification(
                status='error',
                message='No comps found with selected criteria'
            )

        return comps

    # @timeit
    def get_nearby_comps(self, limit=10):
        """
        Get nearby comparatives
        :param limit: The limit of objects list
        """
        return self._get_nearby_comps_query(limit).all()

    def compute_cma(self, comps=None, nearby=False):
        """
        Compute CMA entry point process
        :param comps: The list of subject comparatives to analyze
        :param nearby: Whether compute for the nearby comparatives
        """
        # check if passes subject sale rule
        self.subject_property.passed_subject_sale_rule = self.passed_subject_sale_rule()

        self.sold_withing_date_range_disqualified_sale_alert()
        self.sold_after_date_range_higher_assessment_alert()

        no_assessment = not self.subject_property.assessments
        no_assessment_value = not any(a.value for a in self.subject_property.assessments)

        if self.subject_property.geo is None:
            reference_property = Property.query.get(self.subject_property.reference_building)
            if reference_property and reference_property.geo is not None:
                self.subject_property.geo = reference_property.geo
                self.subject_property.latitude = reference_property.latitude
                self.subject_property.longitude = reference_property.longitude
        no_geo = self.subject_property.geo is None

        if no_assessment or no_assessment_value or no_geo:
            raise exceptions.SubjectLacksDataException('Subject lacks either assessment, latitude or longitude')

        if nearby:
            suitable_comps = self.get_nearby_comps()
        else:
            suitable_comps = self.get_suitable_comps()
        comparatives = self._with_proximity(suitable_comps)

        comparatives = get_whitelisted(comparatives)
        comparatives = self._override_comps(query_comps=comparatives, updated_comps=comps)

        # check if subject can be passed as a comp
        comparatives = self.subject_as_comp(comparatives)

        # if we need to prioritize comparable water categories
        comparatives = self.prioritize_same_water_categories(comparatives)

        # get proper condos
        if self.subject_property.is_condo:
            comparatives = self.apply_condo_logic(comparatives)

        # apply subject age filter
        comparatives = self.subject_age_filter(comparatives)

        self.analyse_comps(comparatives)

    def _with_proximity(self, comps):
        comps_with_proximity = []
        for comp in comps:
            c = comp[0]
            c.proximity = comp[1] / 1609.0
            if c not in comps_with_proximity:
                comps_with_proximity.append(c)

        return comps_with_proximity

    def get_formatted_cma_log(self):
        """
        Get formatted CMA log
        """
        log = self.query_filter.cma_log
        filters = list(log.keys())
        result = {}
        rules = []
        comps = []
        for key, value in log.items():
            rule = dict(rule_key=key,
                        enabled=value['enabled'],
                        comps_count=value['before_count'],
                        comps_removed=value['removed'],
                        comps_added=value.get('added_count'))
            rules.append(rule)
            if value['filtered_comps']:
                filtered_comps = value['filtered_comps']
                for comp in filtered_comps:
                    comp['rules'] = filters[:filters.index(key)]
                    comp['remove_reason'] = key
                    comps.append(comp)
            if value.get('added_from_next_category_comps'):
                added_comps = value['added_from_next_category_comps']
                for comp in added_comps:
                    comp['added_reason'] = key
                    comps.append(comp)
            if value.get('passed_comps'):
                passed_comps = value['passed_comps']
                for comp in passed_comps:
                    comp['remove_reason'] = None
                    comps.append(comp)
        result['rules'] = rules
        result['comps'] = comps
        return result

    def _override_comps(self, query_comps, updated_comps):
        """
        Override query comparatives with updated ones
        """
        # this is a list of comps that need to be analyzed
        # compare the list of query comps returned from the database
        # with the list of changed comps received in the CMA post request

        # if comparative is present in both lists, then we take the changed one from 'comps'
        # otherwise it’s a completely new comp and we include it in the result list for analysis
        comparatives = []
        if updated_comps:

            for suitable in query_comps:
                # get the first comp from the list that has same 'id', and returns None if no item matches
                comp = next((x for x in updated_comps if x.id == suitable.id), None)
                if comp:
                    comparatives.append(comp)
                else:
                    comparatives.append(suitable)
        else:
            comparatives = query_comps

        return comparatives

    def _get_adjusted_market_value_cos(self, comp):
        if hasattr(comp, 'adjusted_market_value') and hasattr(comp, 'adjustment_delta_value_cos'):
            return comp.adjusted_market_value - abs(comp.adjustment_delta_value_cos)
        return None

    def analyse_comp(self, comp):
        comp.last_sale_price = self._get_last_sale_price(comp)
        comp.last_sale_date = self._get_last_sale_date(comp)

        status, adjustment_delta_value, adjustment_results, messages = \
            self.rules_controller.adjust_property(self.subject_property, comp)

        # adjusted comparative market value
        adjusted_market_value = self._get_last_sale_price(comp) + adjustment_delta_value

        # proximity = db.session.query(func.ST_DistanceSphere(comp.geo, self.subject_property.geo)).first()
        # proximity = comp.proximity

        # extend dynamically Property model with extra fields
        comp.adjustment_delta_value = adjustment_delta_value
        comp.adjusted_market_value = adjusted_market_value
        comp.adjustments = adjustment_results
        comp.adjusted_market_value_cos = self._get_adjusted_market_value_cos(comp)

        # comp.obso_result = obso_result

        comp.comp_assessment_value = self._get_comp_assessment_value(comp)
        comp.comp_market_value = self.get_market_value(comp.comp_assessment_value, self.assessment_ratio)

        # set the comparative status: "good" or "bad" or "fail"
        if self.subject_property.county in County.get_florida_counties():
            compare_to = comp.adjusted_market_value_cos
        else:
            compare_to = comp.adjusted_market_value
        comp.status = self._get_comp_status(compare_to, adjustment_status=status, comp=comp)
        return comp

    # @timeit
    def analyse_comps(self, comps, good_count=0):
        """
        Analyse subject comparatives
        """
        mass_cma_limit = 20  # Default good comps limit. If found 20 good comps stop analysing.

        # dynamically extend subject property with additional attributes
        # the same fields must be included in related marshmallow mapping schema to take effect
        self.subject_property.last_sale_price = self._get_last_sale_price(self.subject_property)
        self.subject_property.last_sale_date = self._get_last_sale_date(self.subject_property)
        self.subject_property.print_sale_info = self._get_print_sale_info()

        age_comps = []
        rest_comps = []

        # first analyze the recently_build comps
        if self.subject_property.recently_build:
            recently_build_comps = [comp for comp in comps if comp.recently_build]
            # recently_build_comps.sort(key=lambda c: c.proximity)
            for comp in recently_build_comps:
                self.analyse_comp(comp)
                if comp.status == CompsStatus.GOOD:
                    good_count += 1
                    age_comps.append(comp)
                if self.mass_cma and good_count >= mass_cma_limit:
                    break

        for comp in comps:
            if self.mass_cma and good_count >= mass_cma_limit:
                break

            # if comp already analyzed skip it
            if self.subject_property.recently_build and comp.recently_build:
                if getattr(comp, 'status', None) != CompsStatus.GOOD:
                    rest_comps.append(comp)
                continue

            self.analyse_comp(comp)
            rest_comps.append(comp)

            if comp.status == CompsStatus.GOOD:
                good_count += 1

        if self.subject_property.recently_build and len(age_comps):
            # age_comps.sort(key=lambda c: c.age)
            self._all_comps = age_comps + rest_comps
        else:
            self._all_comps = rest_comps

        # apply the subdivision logic
        self.subdivision_logic()

        if not self.mass_cma:
            for i, comp in enumerate(self._all_comps):
                comp.priority = i

        print(f'{CompsStatus.GOOD} comps count: {len(self.get_good_comps())}')
        print(f'{CompsStatus.BAD} comps count: {len(self.get_bad_comps())}')
        # self.get_good_comps()
        # self.get_bad_comps()
        return None

    def subdivision_logic(self):
        """
        If condo subdivision logic is slightly more complicated
        """
        if self.subject_property.county not in County.get_florida_counties():
            return

        if self.subject_property.is_condo:
            self.subdivision_logic_for_condo()
        else:
            self.subdivision_logic_for_house()

    def subdivision_logic_for_house(self):
        """
        Subdivision logic function for house properties (not condo ones)
        """
        same_subdivision_comps = []
        rest_comps = []
        for comp in self._all_comps:
            if comp.apn[:8] == self.subject_property.apn[:8]:
                same_subdivision_comps.append(comp)
            else:
                rest_comps.append(comp)
        self._all_comps = same_subdivision_comps + rest_comps
        return

    def subdivision_logic_for_condo(self):
        nearby_condos = self._all_comps
        # nearby_condos = [c for c in self._all_comps if c.proximity <= .25]
        # farby_condos = [c for c in self._all_comps if c.proximity > .25]

        self._all_comps = (
            self.subdivision_logic_for_nearby_condos(nearby_condos)  # +
            # self.subdivision_logic_for_farby_condos(farby_condos)
        )
        return

    def subdivision_logic_for_nearby_condos(self, comps):
        """
        Subdivision logic for condos within .25 miles
        """
        subject = self.subject_property

        # define order lists we gonna join in the end
        s_g_b_f_h_v = []
        s_g_b_f_h = []
        s_g_b_f_v = []
        s_g_b_f = []
        s_g_b_h_v = []
        s_g_b_h = []
        s_g_b_v = []
        s_g_b = []
        s_g_f_h_v = []
        s_g_f_h = []
        s_g_f_v = []
        s_g_f = []
        s_g_h_v = []
        s_g_h = []
        s_g_v = []
        s_g = []
        s_b_f_h_v = []
        s_b_f_h = []
        s_b_f_v = []
        s_b_f = []
        s_b_h_v = []
        s_b_h = []
        s_b_v = []
        s_b = []
        s_f_h_v = []
        s_f_h = []
        s_f_v = []
        s_f = []
        s_h_v = []
        s_h = []
        s_v = []
        s = []
        g_b_f_h_v = []
        g_b_f_h = []
        g_b_f_v = []
        g_b_f = []
        g_b_h_v = []
        g_b_h = []
        g_b_v = []
        g_b = []
        g_f_h_v = []
        g_f_h = []
        g_f_v = []
        g_f = []
        g_h_v = []
        g_h = []
        g_v = []
        g = []
        b_f_h_v = []
        b_f_h = []
        b_f_v = []
        b_f = []
        b_h_v = []
        b_h = []
        b_v = []
        b = []
        f_h_v = []
        f_h = []
        f_v = []
        f = []
        h_v = []
        h = []
        v = []
        rest = []

        for comp in comps:
            # if bedroom subdivision bath half_bath view_code
            if (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_g_b_f_h_v.append(comp)

            # elif bedroom subdivision bath half_bath
            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                s_g_b_f_h.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_g_b_f_v.append(comp)

            # elif bedroom subdivision bath
            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp.subject)
            ):
                s_g_b_f.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_g_b_h_v.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                s_g_b_h.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_g_b_v.append(comp)

            # elif bedroom subdivision
            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject)
            ):
                s_g_b.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_g_f_h_v.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                s_g_f_h.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_g_f_v.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_full_baths(comp, subject)
            ):
                s_g_f.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_g_h_v.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                s_g_h.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_g_v.append(comp)

            # elif bedroom
            elif (
                    equal_subdivision(comp, subject) and
                    equal_gla_sqft(comp, subject)
            ):
                s_g.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_b_f_h_v.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                s_b_f_h.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_b_f_v.append(comp)

            # elif subdivision bath half_bath view_code
            elif (
                    equal_subdivision(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject)
            ):
                s_b_f.append(comp)

            # elif subdivision bath half_bath
            elif (
                    equal_subdivision(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_b_h_v.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                s_b_h.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_b_v.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_bedrooms(comp, subject)
            ):
                s_b.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_f_h_v.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                s_f_h.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_f_v.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_full_baths(comp, subject)
            ):
                s_f.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_h_v.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                s_h.append(comp)

            elif (
                    equal_subdivision(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                s_v.append(comp)

            # elif subdivision
            elif (
                    equal_subdivision(comp, subject)
            ):
                s.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                g_b_f_h_v.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                g_b_f_h.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                g_b_f_v.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject)
            ):
                g_b_f.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                g_b_h_v.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                g_b_h.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                g_b_v.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_bedrooms(comp, subject)
            ):
                g_b.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                g_f_h_v.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                g_f_h.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                g_f_v.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_full_baths(comp, subject)
            ):
                g_f.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                g_h_v.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                g_h.append(comp)

            elif (
                    equal_gla_sqft(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                g_v.append(comp)

            elif (
                    equal_gla_sqft(comp, subject)
            ):
                g.append(comp)

            elif (
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                b_f_h_v.append(comp)

            elif (
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                b_f_h.append(comp)

            elif (
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                b_f_v.append(comp)

            elif (
                    equal_bedrooms(comp, subject) and
                    equal_full_baths(comp, subject)
            ):
                b_f.append(comp)

            elif (
                    equal_bedrooms(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                b_h_v.append(comp)

            elif (
                    equal_bedrooms(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                b_h.append(comp)

            elif (
                    equal_bedrooms(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                b_v.append(comp)

            elif (
                    equal_bedrooms(comp, subject)
            ):
                b.append(comp)

            # elif bath half_bath view_code
            elif (
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                f_h_v.append(comp)

            # elif bath half_bath
            elif (
                    equal_full_baths(comp, subject) and
                    equal_half_baths(comp, subject)
            ):
                f_h.append(comp)

            # elif bath half_bath
            elif (
                    equal_full_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                f_v.append(comp)

            # elif bath
            elif (
                    equal_full_baths(comp, subject)
            ):
                f.append(comp)

            # elif half_bath view_code
            elif (
                    equal_half_baths(comp, subject) and
                    equal_view_condo_category(comp, subject)
            ):
                h_v.append(comp)

            # elif half_bath
            elif (
                    equal_half_baths(comp, subject)
            ):
                h.append(comp)

            # elif view_code
            elif (
                    equal_view_condo_category(comp, subject)
            ):
                v.append(comp)

            # else append to rest
            else:
                rest.append(comp)

        combined = (
                s_g_b_f_h_v +
                s_g_b_f_h +
                s_g_b_f_v +
                s_g_b_f +
                s_g_b_h_v +
                s_g_b_h +
                s_g_b_v +
                s_g_b +
                s_g_f_h_v +
                s_g_f_h +
                s_g_f_v +
                s_g_f +
                s_g_h_v +
                s_g_h +
                s_g_v +
                s_g +
                s_b_f_h_v +
                s_b_f_h +
                s_b_f_v +
                s_b_f +
                s_b_h_v +
                s_b_h +
                s_b_v +
                s_b +
                s_f_h_v +
                s_f_h +
                s_f_v +
                s_f +
                s_h_v +
                s_h +
                s_v +
                s +
                g_b_f_h_v +
                g_b_f_h +
                g_b_f_v +
                g_b_f +
                g_b_h_v +
                g_b_h +
                g_b_v +
                g_b +
                g_f_h_v +
                g_f_h +
                g_f_v +
                g_f +
                g_h_v +
                g_h +
                g_v +
                g +
                b_f_h_v +
                b_f_h +
                b_f_v +
                b_f +
                b_h_v +
                b_h +
                b_v +
                b +
                f_h_v +
                f_h +
                f_v +
                f +
                h_v +
                h +
                v +
                rest
        )

        return combined

    # def subdivision_logic_for_farby_condos(self, comps):
    #     """
    #     Subdivision logic for condos further .25 miles
    #     """
    #     subject = self.subject_property
    #
    #     # define order lists we gonna join in the end
    #     s_b_f_h_v = []
    #     s_b_f_h = []
    #     s_b_f_v = []
    #     s_b_f = []
    #     s_b_h_v = []
    #     s_b_h = []
    #     s_b_v = []
    #     s_b = []
    #     s_f_h_v = []
    #     s_f_h = []
    #     s_f_v = []
    #     s_f = []
    #     s_h_v = []
    #     s_h = []
    #     s_v = []
    #     s = []
    #     b_f_h_v = []
    #     b_f_h = []
    #     b_f_v = []
    #     b_f = []
    #     b_h_v = []
    #     b_h = []
    #     b_v = []
    #     b = []
    #     f_h_v = []
    #     f_h = []
    #     f_v = []
    #     f = []
    #     h_v = []
    #     h = []
    #     v = []
    #     rest = []
    #
    #     for comp in comps:
    #         if (
    #                 equal_subdivision(comp, subject) and
    #                 equal_bedrooms(comp, subject) and
    #                 equal_full_baths(comp, subject) and
    #                 equal_half_baths(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             s_b_f_h_v.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject) and
    #                 equal_bedrooms(comp, subject) and
    #                 equal_full_baths(comp, subject) and
    #                 equal_half_baths(comp, subject)
    #         ):
    #             s_b_f_h.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject) and
    #                 equal_bedrooms(comp, subject) and
    #                 equal_full_baths(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             s_b_f_v.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject) and
    #                 equal_bedrooms(comp, subject) and
    #                 equal_full_baths(comp, subject)
    #         ):
    #             s_b_f.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject) and
    #                 equal_bedrooms(comp, subject) and
    #                 equal_half_baths(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             s_b_h_v.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject) and
    #                 equal_bedrooms(comp, subject) and
    #                 equal_half_baths(comp, subject)
    #         ):
    #             s_b_h.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject) and
    #                 equal_bedrooms(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             s_b_v.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject) and
    #                 equal_bedrooms(comp, subject)
    #         ):
    #             s_b.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject) and
    #                 equal_full_baths(comp, subject) and
    #                 equal_half_baths(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             s_f_h_v.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject) and
    #                 equal_full_baths(comp, subject) and
    #                 equal_half_baths(comp, subject)
    #         ):
    #             s_f_h.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject) and
    #                 equal_full_baths(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             s_f_v.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject) and
    #                 equal_full_baths(comp, subject)
    #         ):
    #             s_f.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject) and
    #                 equal_half_baths(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             s_h_v.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject) and
    #                 equal_half_baths(comp, subject)
    #         ):
    #             s_h.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             s_v.append(comp)
    #
    #         elif (
    #                 equal_subdivision(comp, subject)
    #         ):
    #             s.append(comp)
    #
    #         elif (
    #                 equal_bedrooms(comp, subject) and
    #                 equal_full_baths(comp, subject) and
    #                 equal_half_baths(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             b_f_h_v.append(comp)
    #
    #         elif (
    #                 equal_bedrooms(comp, subject) and
    #                 equal_full_baths(comp, subject) and
    #                 equal_half_baths(comp, subject)
    #         ):
    #             b_f_h.append(comp)
    #
    #         elif (
    #                 equal_bedrooms(comp, subject) and
    #                 equal_full_baths(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             b_f_v.append(comp)
    #
    #         elif (
    #                 equal_bedrooms(comp, subject) and
    #                 equal_full_baths(comp, subject)
    #         ):
    #             b_f.append(comp)
    #
    #         elif (
    #                 equal_bedrooms(comp, subject) and
    #                 equal_half_baths(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             b_h_v.append(comp)
    #
    #         elif (
    #                 equal_bedrooms(comp, subject) and
    #                 equal_half_baths(comp, subject)
    #         ):
    #             b_h.append(comp)
    #
    #         elif (
    #                 equal_bedrooms(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             b_v.append(comp)
    #
    #         elif (
    #                 equal_bedrooms(comp, subject)
    #         ):
    #             b.append(comp)
    #
    #         elif (
    #                 equal_full_baths(comp, subject) and
    #                 equal_half_baths(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             f_h_v.append(comp)
    #
    #         # elif bath half_bath
    #         elif (
    #                 equal_full_baths(comp, subject) and
    #                 equal_half_baths(comp, subject)
    #         ):
    #             f_h.append(comp)
    #
    #         elif (
    #                 equal_full_baths(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             f_v.append(comp)
    #
    #         # elif bath
    #         elif (
    #                 equal_full_baths(comp, subject)
    #         ):
    #             f.append(comp)
    #
    #         # elif half_bath view_code
    #         elif (
    #                 equal_half_baths(comp, subject) and
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             h_v.append(comp)
    #
    #         # elif half_bath
    #         elif (
    #                 equal_half_baths(comp, subject)
    #         ):
    #             h.append(comp)
    #
    #         # elif view_code
    #         elif (
    #                 equal_view_condo_category(comp, subject)
    #         ):
    #             v.append(comp)
    #
    #         # else append to rest
    #         else:
    #             rest.append(comp)
    #
    #     combined = (
    #             s_b_f_h_v +
    #             s_b_f_h +
    #             s_b_f_v +
    #             s_b_f +
    #             s_b_h_v +
    #             s_b_h +
    #             s_b_v +
    #             s_b +
    #             s_f_h_v +
    #             s_f_h +
    #             s_f_v +
    #             s_f +
    #             s_h_v +
    #             s_h +
    #             s_v +
    #             s +
    #             b_f_h_v +
    #             b_f_h +
    #             b_f_v +
    #             b_f +
    #             b_h_v +
    #             b_h +
    #             b_v +
    #             b +
    #             f_h_v +
    #             f_h +
    #             f_v +
    #             f +
    #             h_v +
    #             h +
    #             v +
    #             rest
    #     )
    #
    #     return combined

    def _get_last_sale_price(self, prop):
        """
        Get last property sale price
        """
        if hasattr(prop, 'last_sale_price'):
            return prop.last_sale_price

        if prop.last_sale:
            return prop.last_sale.price
        return None

    def _get_last_sale_date(self, prop):
        """
        Get last property sale date
        """
        if hasattr(prop, 'last_sale_date'):
            return prop.last_sale_date

        if prop.last_sale:
            return prop.last_sale.date
        return None

    def _get_comp_assessment_value(self, comparative) -> Union[int, None]:
        """
        Get correct comparative assessment value
        """
        if comparative and comparative.assessments and comparative.assessments[0]:
            return comparative.assessments[0].value
        return None

    def _get_comp_status(self, adjusted_market_value, adjustment_status, comp):
        """
        Get comparative status depending on adjusted market value & proximity
        :param adjusted_market_value: The adjusted comparative market value or
        adjusted cos market value if county is a florida county
        :param adjustment_status: The adjustments status
        """
        # case subject as a comp
        if comp.id == self.subject_property.id:
            if self.subject_property.passed_subject_sale_rule:
                return CompsStatus.GOOD
            else:
                return CompsStatus.BAD

        # define comp status
        if adjustment_status:
            if adjusted_market_value and adjusted_market_value < self.subject_property.market_value:
                return CompsStatus.GOOD
            else:
                return CompsStatus.BAD

        return CompsStatus.FAIL

    def _get_total_market_value(self, comps):
        """
        Get total comparative market value
        :param comps: The list of subject comparatives
        """
        if self.subject_property.county in County.get_florida_counties():
            return sum(comp.adjusted_market_value_cos for comp in comps)
        return sum(comp.adjusted_market_value for comp in comps)

    def get_claimed_market_value(self, comps) -> Union[None, float]:
        """
        Get claimed market value.
        The average of comparative 'adjusted_market_value'.

        :param comps: The list of subject comparatives
        """
        if not comps:
            return None

        total_market_value = self._get_total_market_value(comps)
        count = len(comps)

        return int(total_market_value / count)

    def get_proposed_assessment_value(self, comps, claimed_market_value=None) -> Union[None, int]:
        """
        Get proposed assessment value.
        Formula:
            result = 'claimed_market_value' * ratio

        :param comps: The list of subject comparatives
        :param claimed_market_value: The average of comparative 'adjusted_market_value'.
        """
        if not comps:
            return None

        # get claimed market value
        if not claimed_market_value:
            claimed_market_value = self.get_claimed_market_value(comps)

        # calculate requested new assessment value
        new_assessment_value = round(claimed_market_value * float(self.assessment_ratio))

        return new_assessment_value

    def _get_print_sale_info(self) -> Union[None, bool]:
        """
        Get print sale info.
        Check whether subject last sale date is greater than 'subject_sales_from' date in properties rules.
        """
        if self.subject_property.last_sale is None or self.subject_property.last_sale.date is None or \
                self.properties_rules.subject_sales_from is None:
            return None
        return self.subject_property.last_sale.date > self.properties_rules.subject_sales_from

    def get_all_avg_comps(self, amount: int = 4):
        combined_list = self._good_comps[:amount]
        if len(combined_list) < amount:
            lacking_amount = amount - len(combined_list)
            combined_list.extend(self._bad_comps[:lacking_amount])
        return combined_list

    def get_all_comps(self):
        """
        Get all subject comparatives.
        """
        return self._all_comps

    def _get_status_comps(self, status):
        """
        Get comparatives by status name
        """

        # mass cma comps may miss status because we stop analysing at 20 good comps
        return [c for c in self._all_comps if getattr(c, 'status', None) == status]

    def get_good_comps(self, amount=None):
        """
        Get first subject good comparatives.
        :param amount: The amount of good comps to get or None
        """
        # get all good comparatives
        self._good_comps = self._get_status_comps(status=CompsStatus.GOOD)

        if amount:
            return self._good_comps[:amount]
        return self._good_comps

    def get_bad_comps(self, amount=None):
        """
        Get first subject bad comparatives.
        :param amount: The amount of bad comps to get or None
        """
        self._bad_comps = self._get_status_comps(status=CompsStatus.BAD)
        if amount:
            return self._bad_comps[:amount]
        return self._bad_comps

    def get_good_bad_comps(self, amount=None):
        """
        Get first subject good and bad comparatives.
        :param amount: The amount of good and bad comps sorted by proximity to get or None
        """
        self._good_bad_comps = self._all_comps
        if amount:
            return self._good_bad_comps[:amount]
        return self._good_bad_comps

    def get_waterfront_comps(self, comps):
        """
        Mass CMA:
        - Find a total of 12 comps (good or bad) in the same category
        - If less than 12, then pick the lower tier category. Category 5 is the final, do not go lower
        - If less than 12 comps, and we started at Category 5 - go up instead of down,
        one by one until 12 comps reached
        - If we are at category 6 and less than 12,
        then seek the comps that do not have water_category at all (land comps)
        """
        subject_category = self.subject_property.water_category

        # filter same category amount
        category = self.subject_property.water_category
        same_category_comps = [c for c in comps if c.water_category == subject_category]
        added_from_next_category_comps = []
        while len(same_category_comps) < 12:
            next_category = get_next_water_category(category, subject_category)
            if next_category == -1:
                return same_category_comps, added_from_next_category_comps
            next_category_comps = [c for c in comps if c.water_category == next_category]
            added_from_next_category_comps += next_category_comps
            same_category_comps += next_category_comps
            category = next_category
        return same_category_comps, added_from_next_category_comps

    def get_requested_assessment_range_values(self, amount_ranges: list = None):
        """
        Get a list of requested new assessment values in the list of ranges
        :param amount_ranges: The list of ranges

        Result object:
            {
                'misc': {'range<amount>: proposed_assessment_value, ...},
                'good': {'range<amount>: proposed_assessment_value, ...},
            }
        """
        # get all average ranges: 'misc' & 'good'
        # 'misc' means that in the list can be good or bad comparatives
        # 'good' means that in the list can be only good comparatives
        average_ranges = self.get_all_avg_ranges(amount_ranges=amount_ranges)

        values = {}
        for ar_type in average_ranges.keys():
            values[ar_type] = {r: v.get('proposed_assessment_value') for r, v in average_ranges[ar_type].items()}

        return values

    def get_all_avg_ranges(self, amount_ranges: list = None):
        """
        Get all average ranges for 'misc' & 'good' comps
        :param amount_ranges: The list of ranges
        """
        avg_ranges = {
            'misc': self.get_misc_avg_ranges(amount_ranges),
            'good': self.get_good_avg_ranges(amount_ranges)
        }

        return avg_ranges

    def get_subject_good_sale_value(self):
        if self.subject_assessment and self.subject_assessment.assessment_value and self.delta:
            return self.subject_assessment.assessment_value - self.delta
        return None

    def get_subject_good_sale_ranges(self, amount_ranges=None):
        if amount_ranges is None:
            amount_ranges = [4, 8, 12]

        avg_ranges = {}
        value = self.get_subject_good_sale_value()
        for amount in amount_ranges:
            # dynamically create range fields
            avg_ranges[str(amount)] = {
                'proposed_assessment_value': value,
                'claimed_market_value': value,
            }

        all_ranges = {
            'misc': avg_ranges,
            'good': avg_ranges
        }
        return all_ranges

    def _get_avg_ranges(self, fn, amount_ranges: list = None):
        """
        Get average ranges for callable.
        :param fn: The callable function to get comps
        :param amount_ranges: The list of ranges
        """
        # define default range list
        if amount_ranges is None:
            amount_ranges = [4, 8, 12]

        avg_ranges = {}
        for amount in amount_ranges:
            comps = fn(amount)
            claimed_market_value = self.get_claimed_market_value(comps)
            # dynamically create range fields
            avg_ranges[str(amount)] = {
                'proposed_assessment_value': self.get_proposed_assessment_value(comps, claimed_market_value),
                'claimed_market_value': claimed_market_value,
            }
        return avg_ranges

    def get_misc_avg_ranges(self, amount_ranges: list = None):
        """
        Get average ranges for good or bad comparatives
        :param amount_ranges: The list of ranges
        """
        return self._get_avg_ranges(self.get_good_bad_comps, amount_ranges)

    def get_good_avg_ranges(self, amount_ranges: list = None):
        """
        Get average ranges for good only comparatives.
        :param amount_ranges: The list of ranges
        """
        return self._get_avg_ranges(self.get_good_comps, amount_ranges)

    def get_derived_assessment_results(self):
        """
        Get derived assessment results:
            * current market value
            * current assessment value
            * requested new assessment value
            * claimed market value
            * tax value
        """

        # try to get the default amount of comps
        comps = self.get_all_avg_comps(self.DEFAULT_COMPS_AMOUNT)

        # not enough comps, throw the exception
        if len(comps) < self.REQUIRED_COMPS_AMOUNT:
            raise exceptions.NotEnoughCompsException(
                "Subject has only {} comps instead of {} required".format(len(comps), self.REQUIRED_COMPS_AMOUNT)
            )

        claimed_market_value = self.get_claimed_market_value(comps)
        proposed_assessment_value = self.get_proposed_assessment_value(comps)

        derived_results = {
            'current_market_value': self.subject_property.market_value,
            'current_assessment_value': self.subject_assessment.assessment_value,
            'override_assessment_value': self.assessment_value,
            'proposed_assessment_value': proposed_assessment_value,
            'claimed_market_value': claimed_market_value,
            'tax_value': proposed_assessment_value,  # TODO: Awaiting Tax Ratios info from the client
            'assessment_ratio': float(self.assessment_ratio),
        }

        return derived_results
