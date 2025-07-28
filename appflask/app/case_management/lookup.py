from abc import ABC, abstractmethod

from app import db


class EntityName:
    CASE = 'case_property'
    CLIENT = 'case_client'


class Operator:
    EQ = '='
    GT = '>'
    GTE = '>='
    LT = '<'
    LTE = '<='
    IN = 'in'
    TS_QUERY = "@@"
    IS = "is"


class DataType:
    STRING = "string"
    DATE = "date"
    NUMERIC = "numeric"
    BOOL = "boolean"


class LookupEntities(ABC):
    """
    Lookup entities for list of filters

    Structure of each filter must be:
        - key: The attribute(s) in a DB table
        - value: The value(s) of filter to apply
        - entity: The name of the table in DB
        - operator: The operation to apply for the filter
        - type: The type of data or filter

    Examples:
    [
        {
            "key": "id",
            "value": [
                1,
                2,
                3
            ],
            "entity": "case_tag",
            "operator": "in"
            "type": "numeric"
        },
        {
            "key": "id",
            "value": 1,
            "entity": "case_marketing_code",
            "operator": "=",
            "type": "numeric"
        },
        {
            "key": "county",
            "value": "broward",
            "entity": "case_application",
            "operator": "=",
            "type": "string"
        },
        {
            "key": [
                "phone_number_1",
                "phone_number_2",
                ],
            "value": "5445",
            "entity": "case_client",
            "operator": "=",
            "type": "string"
        },
    ]
    """
    def __init__(self, filters):
        self.filters = filters
        self.query = ''
        self.result_proxy = []

    # entity aliases for join purpose
    aliases = {
        "case_client": "cc",
        "case_client_type": "cc_type",
        "case_marketing_code": "cmc",
        "property": "p",
        "case_property": "cp",
        "case_application": "ca",
        "case_client_tag": "cc_tag",
        "case_tag": "ct",
        "case_note": "cn",
        "case_billing": "cb",
        "case_email": "ce",
        "case_payment_status": "cps",
        "case_payment_type": "cpt",
        "single_cma_workups": "ssw"
    }

    @abstractmethod
    def make_joins(self):
        """
        Make sql statement with required entities joins using mapped aliases
        """
        pass

    def _make_date_clause(self, alias, key, value, operator: Operator):
        """
        Make date type clause
        """
        if operator not in (Operator.GT, Operator.GTE, Operator.LT, Operator.LTE, Operator.EQ):
            raise ValueError("Invalid date operator")

        return f" Date({alias}.{key}) {operator} '{value}'"

    def _make_bool_clause(self, alias, key, value, operator: Operator):
        """
        Make boolean type clause
        """
        if operator != Operator.IS:
            raise ValueError("Invalid bool operator")

        if value is None:
            value = 'null'

        if isinstance(key, list):
            clauses = []
            for k in key:
                clause = f" {alias}.{k} {operator} {str(value).lower()}"
                clauses.append(clause)

            if value:
                result = " or ".join(clauses)
            else:
                result = " and ".join(clauses)
            # for cl in clauses:
            #     result = f" {result} {cl} or"
            return f"({result})"
        else:
            return f" {alias}.{key} {operator} {str(value).lower()}"

    def _handle_ts_query_operator(self, alias, key, value):
        prefix = ''
        if not isinstance(key, list):
            key = [key]

        for k in key:
            prefix = f"{prefix} {alias}.{k}, ' ', "

        # remove last added sufix
        prefix = prefix[:-7]
        prefix = f'concat({prefix})'

        # remove special symbols from value
        splits = []
        for val in value.split(' '):
            alphanumeric = [ch for ch in val if ch.isalnum() or '#']
            val = "".join(alphanumeric)

            if val == "":
                continue
            splits.append(val)

        if len(splits) == 1:
            list_value = splits[0]
        else:
            list_value = ' & '.join(splits)
        clause = f" to_tsvector({prefix}) @@ to_tsquery('{list_value}')"
        return clause

    def _handle_in_operator(self, alias, key, value):
        """
        Create query condition for the SQL 'IN' operator
        """
        if not isinstance(value, list):
            raise ValueError("Invalid value for 'IN' operator")

        # the value is a list of 2+ elements, simple convert from [] to () braces
        if len(value) > 1:
            clause = f" {alias}.{key} {Operator.IN} {tuple(value)}"
        else:
            # the only one value in a list, add () manually
            clause = f" {alias}.{key} {Operator.IN} ({value[0]})"

        return clause

    def _handle_eq_single_key(self, alias, key, value):
        if isinstance(value, str):
            # handle string

            if key == '_property_type':
                clause = f"'{value}' = case" \
                         f" when (p.property_class = 0) then 'vacant' " \
                         f" when (p.is_condo is true) then 'condo'      " \
                         f" else 'residential'" \
                         f" end"
            else:
                clause = f" lower({alias}.{key}) {Operator.EQ} '{value.lower()}'"
        else:
            # handle numeric
            clause = f" {alias}.{key} {Operator.EQ} {value}"
        return clause

    def _handle_eq_operator(self, alias, key, value):
        if isinstance(key, list):
            conditions = []
            for k in key:
                condition = self._handle_eq_single_key(alias, k, value)
                conditions.append(condition)
            clause = " or ".join(conditions)

        else:
            clause = self._handle_eq_single_key(alias, key, value)
        return clause

    def _handle_compare_operator(self, alias, key, value, operator):
        clause = f" {alias}.{key} {operator} {value}"
        return clause

    def make_clause(self, entity, key, value, operator: Operator, data_type):
        """
        Make query filter clause
        """
        # get table alias
        alias = self.aliases.get(entity)

        # handle 'date' type
        if data_type and data_type == DataType.DATE:
            clause = self._make_date_clause(alias, key, value, operator)

        # handle 'boolean' type
        elif data_type and data_type == DataType.BOOL:
            clause = self._make_bool_clause(alias, key, value, operator)
        else:
            if operator == Operator.EQ:
                clause = self._handle_eq_operator(alias, key, value)
            elif operator == Operator.IN:
                clause = self._handle_in_operator(alias, key, value)
            elif operator in (Operator.LTE, Operator.LT, Operator.GTE, Operator.GT):
                clause = self._handle_compare_operator(alias, key, value, operator)
            elif operator == Operator.TS_QUERY:
                clause = self._handle_ts_query_operator(alias, key, value)
            else:
                raise ValueError("Invalid operator")

        return f'({clause})'

    def lookup(self):
        """
        Entry point to lookup entities, return a list of unique entity ID's
        """
        # make required joins with target entity
        self.make_joins()

        if not self.filters:
            self.result_proxy = db.session.execute(self.query)
            return self

        # have filters, construct where conditions
        self.query = f"{self.query} where"

        # parse and apply filters
        clauses = []
        for filter_obj in self.filters:
            entity = filter_obj.get('entity')
            key = filter_obj.get('key')
            value = filter_obj.get('value')
            operator = filter_obj.get('operator')
            data_type = filter_obj.get('type')

            # multiple entities handling
            if isinstance(entity, list):
                cases = []
                for e in entity:
                    cases.append(self.make_clause(e, key, value, operator, data_type))
                clause = ' or '.join(cases)
                clause = f"({clause})"
            else:
                # make filter clause
                clause = self.make_clause(entity, key, value, operator, data_type)

            # first condition without 'and' operand
            if not clauses:
                clause = f"{clause}"
            else:
                clause = f" and {clause}"
            clauses.append(clause)

        # construct final query with all filter conditions
        for c in clauses:
            self.query = f"{self.query} {c}"

        print('Query conditions:', clauses)
        print('Query:', self.query)

        self.result_proxy = db.session.execute(self.query)
        return self

    def serialize(self):
        """
        Transform 'ResultProxy' object to dictionary
        """
        obj, objects = {}, []
        for row_proxy in self.result_proxy:
            # row_proxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in row_proxy.items():
                # build up the dictionary
                obj = {**obj, **{column: value}}
            objects.append(obj)

        return objects


class LookupClients(LookupEntities):

    def make_joins(self):
        """
        Make 'case_client' SQL left joins
        When you add new table to join, be sure you add a new alias into lookup aliases
        """
        self.query = '''
                        select distinct(cc.id) from case_client cc
                            left join case_application ca on cc.id = ca.client_id
                            left join case_property cp on cp.client_id = cc.id
                            left join single_sma_workups ssw on cp.id = ssw.case_property_id
                            left join case_email ce on cc.email_id = ce.id
                            left join property p on cp.property_id = p.id
                            left join case_client_type cc_type on cc.type_id = cc_type.id
                            left join case_marketing_code cmc on cc.marketing_code_id = cmc.id
                            left join case_client_tag cc_tag on cc.id = cc_tag.client_id
                            left join case_tag ct on cc_tag.tag_id = ct.id
                            left join case_note cn on (cc.id = cn.sender_id and cn.sender = 2)
                            left join case_billing cb on cc.billing_id = cb.id
                            left join case_payment_status cps on cp.payment_status_id = cps.id
                            left join case_payment_type cpt on cp.payment_status_id = cpt.id
        '''


class LookupCases(LookupEntities):
    def make_joins(self):
        """
        Make 'case_property' SQL left joins
        When you add new table to join, be sure you add a new alias into lookup aliases
        """
        self.query = '''
                        select distinct(cp.id) from case_property cp
                            left join case_client cc on cp.client_id = cc.id
                            left join single_sma_workups ssw on cp.id = ssw.case_property_id
                            left join case_application ca on ca.case_property_id = cp.id
                            left join case_email ce on cc.email_id = ce.id
                            left join property p on cp.property_id = p.id
                            left join case_client_type cc_type on cc.type_id = cc_type.id
                            left join case_marketing_code cmc on cc.marketing_code_id = cmc.id
                            left join case_client_tag cc_tag on cc.id = cc_tag.client_id
                            left join case_tag ct on cc_tag.tag_id = ct.id
                            left join case_note cn on (cc.id = cn.sender_id and cn.sender = 2)
                            left join case_billing cb on cc.billing_id = cb.id
                            left join case_payment_status cps on cp.payment_status_id = cps.id
                            left join case_payment_type cpt on cp.payment_status_id = cpt.id
        '''
