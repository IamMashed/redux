from sqlalchemy.exc import IntegrityError

from app import db
from my_logger import logger


class UpsertMixin(object):
    @classmethod
    def update_if_exists(cls, object_map):
        obj = cls.query.filter_by(property_id=object_map['property_id'])
        if object_map.get('date'):
            # used when parsing sales
            obj = obj.filter_by(date=object_map.get('date'))
        try:
            if obj.first():  # update if exists
                obj.update({**object_map})
                logger.info(f'updated record with property_id {object_map["property_id"]}')
            else:
                new_obj = cls(**object_map)
                db.session.add(new_obj)
                logger.info(f'record with property_id {object_map["property_id"]} created')
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f'failed to upsert due to {e.orig.args}')
            return e.orig.args
        return None

    @classmethod
    def insert(cls, object_map):
        try:
            new_obj = cls(**object_map)
            # print(f'inserting... {object_map}')
            db.session.add(new_obj)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(f'failed to insert due to {e.orig.args}')
            return e.orig.args
        return None

    @classmethod
    def upsert(cls, object_map):
        """
        Update if exist or insert new.
        """
        obj = cls.query.filter_by(property_id=object_map['property_id'])
        try:
            # update if exists
            if obj.first():
                cls.update_if_exists(object_map)
            # insert new
            else:
                cls.insert(object_map)
        except IntegrityError as e:
            db.session.rollback()
            return e.orig.args
        return None


class ValidationMixin(object):
    @classmethod
    def update_if_exists(cls, apn, county, errors):
        validation = cls.query.filter_by(apn=apn, county=county)
        if validation.first():
            validation.errors = errors
        else:
            new_validation = cls()
            new_validation.apn = apn
            new_validation.county = county
            new_validation.errors = errors
            db.session.add(new_validation)
        db.session.commit()

    @classmethod
    def insert(cls, apn, county, errors):
        new = cls()
        new.apn = apn
        new.county = county
        new.errors = errors
        db.session.add(new)
        db.session.commit()
