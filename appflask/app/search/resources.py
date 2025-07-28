from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy import cast, String, func

from app import db
from app.case_management.models import Client, CaseProperty, Application, CaseEmail, ClientSchema, CasePropertySchema, \
    ApplicationSchema, ApplicationStatus, ClientType
from app.database.models import Property
from app.database.models.property import PropertyModelSchema

# from app.routing.decorators import timeit


class QuickSearchApi(Resource):
    SEARCH_LIMIT = 5

    def make_search_items(self, objects, entity, schema):
        """
        Make response object for searched objects
        """
        items = []
        for o in objects:
            items.append(
                {
                    "entity": entity,
                    "id": o['id'],
                    "name": o['name'],
                    "item": schema().dump(o['model'].query.get(o['id']), many=False)
                }
            )
        return items

    def entities_to_objects(self, entities, model):
        objects = [
            {
                'id': e[0],
                'name': e[1],
                'model': model
            } for e in entities
        ]
        return objects

    # @timeit
    def get_clients(self, search):
        """
        Search client IDs
        """
        filters = [
            Client.case_id.ilike(f'%{search}%'),
            Client.phone_number_1.ilike(f'%{search}%'),
            Client.phone_number_2.ilike(f'%{search}%'),
            Client.full_name.ilike(f'%{search}%'),
        ]

        query = (
            Client.query.with_entities(Client.id, Client.full_name)
            .filter(
                db.or_(
                    *filters
                )
            )
            .filter(Client.type_id == ClientType.CURRENT)
        )

        objects = self.entities_to_objects(entities=query.limit(QuickSearchApi.SEARCH_LIMIT).all(), model=Client)
        return self.make_search_items(objects, entity='case_client', schema=ClientSchema)

    # @timeit
    def get_properties(self, search):
        """
        Search properties IDs
        """
        # https://stackoverflow.com/questions/1566717/postgresql-like-query-performance-variations/1566769#1566769

        # tokenize for tsquery
        search_parts = search.strip().lower().replace(',', '').split()
        address_search = '&'.join(search_parts)

        query = (
            Property.query.with_entities(Property.id, Property.address)
            .filter(
                db.or_(
                    cast(Property.id, String).like(f'%{search}%'),
                    # Property.address.ilike(f'%{search}%'),
                    func.to_tsvector(
                        'english',
                        Property.address
                    ).match(address_search, postgresql_regconfig='english'),
                    Property.apn.ilike(f'%{search}%')

                )
            )
        )
        objects = self.entities_to_objects(entities=query.limit(QuickSearchApi.SEARCH_LIMIT).all(), model=Property)
        return self.make_search_items(objects, entity='property', schema=PropertyModelSchema)

    # @timeit
    def get_case_properties(self, search):
        """
        Search case property IDs
        """
        # case property search filters
        filters = [
            # CaseProperty.full_address.ilike(f'%{search}%'),
            CaseProperty.apn.ilike(f'%{search}%'),
            CaseProperty.case_id.ilike(f'%{search}%'),
            CaseProperty.pin_code.ilike(f'%{search}%')
        ]

        query = (
            CaseProperty.query.with_entities(CaseProperty.id, CaseProperty.full_address)
            .join(Property, isouter=True)
            .filter(
                db.or_(
                    *filters,
                    Property.address.ilike(f'%{search}%')
                )
            )
        )
        # print(query)
        objects = self.entities_to_objects(entities=query.limit(QuickSearchApi.SEARCH_LIMIT).all(), model=CaseProperty)
        return self.make_search_items(objects, entity='case_property', schema=CasePropertySchema)

    # @timeit
    def get_applications(self, search):
        """
        Search applications IDs
        """

        # applications search filters
        filters = [
            Application.full_address.ilike(f'%{search}%'),
            Application.full_name.ilike(f'%{search}%'),
            Application.phone_number_1.ilike(f'%{search}%'),
            Application.phone_number_2.ilike(f'%{search}%'),
            Application.pin_code.ilike(f'%{search}%'),
            CaseEmail.email_address.ilike(f'%{search}%')
        ]

        query = (
            Application.query.with_entities(Application.id, Application.full_address)
            .join(CaseEmail, isouter=True)
            .filter(
                db.or_(
                    *filters
                )
            )
            .filter(Application.status_id.notin_([ApplicationStatus.FULLY_REJECTED, ApplicationStatus.APPROVED]))
        )

        objects = self.entities_to_objects(entities=query.limit(QuickSearchApi.SEARCH_LIMIT).all(), model=Application)
        return self.make_search_items(objects, entity='case_application', schema=ApplicationSchema)

    def get(self):
        search = request.args.get('search', default='', type=str)

        # start search only if at least 3 symbols passed
        if len(search) < 3:
            return jsonify([])

        search_result = self.get_clients(search) + self.get_case_properties(
            search) + self.get_properties(search) + self.get_applications(search)

        return jsonify(search_result)
