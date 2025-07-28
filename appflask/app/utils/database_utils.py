from flask_script import Manager, prompt_bool
from sqlalchemy import create_engine

from app.database import db
from config import SQLALCHEMY_DATABASE_URI

manager = Manager(usage='Perform database operations')


def init_db():
    db.create_all()


def drop_tables():
    db.drop_all()


@manager.command
def create(default_data=True, sample_data=False):
    """Create database tables from models"""
    init_db()
    print("database tables created")


@manager.command
def drop():
    """Drop Database Tables"""
    if prompt_bool("Are you sure you want to lose all your data"):
        drop_tables()
        print("deleted all tables from the database")


@manager.command
def recreate():
    """Recreate database"""
    drop()
    create(default_data=True, sample_data=False)


def _execute_query(query):
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn, conn.begin():
        db.session.execute(query)


@manager.command
def drop_gin_indexes():
    """
    Drop GIN indexes for property table fields:
        - apn
        - id
        - address
        - address_line_1
        - address_line_2
    """

    query = '''
        DROP INDEX property_apn_gin_trgm_idx;
        DROP INDEX property_id_gin_trgm_idx;
        DROP INDEX property_address_gin_idx;
        DROP INDEX property_address_line_1_gin_idx;
        DROP INDEX property_address_line_2_gin_idx;
    '''
    _execute_query(query)
    print('GIN Indexes dropped')


@manager.command
def create_gin_indexes():
    """
    Create GIN indexes for property fields:
        - apn
        - id
        - address
        - address_line_1
        - address_line_2
    """
    query = '''
        -- create 'apn' gin trigram index
        CREATE INDEX property_apn_gin_trgm_idx ON property USING gin (apn gin_trgm_ops);
        ALTER INDEX property_apn_gin_trgm_idx SET (fastupdate = false);

        -- create 'id' gin trigram index
        CREATE INDEX property_id_gin_trgm_idx on property using gin (cast(id as varchar) gin_trgm_ops);
        ALTER INDEX property_id_gin_trgm_idx SET (fastupdate = false);
        -- create 'address' gin index
        CREATE INDEX property_address_gin_idx ON property USING GIN (to_tsvector('english', address));
        -- create 'address_line_1' gin index
        CREATE INDEX property_address_line_1_gin_idx ON property USING GIN (to_tsvector('english', address_line_1));

        -- create 'address_line_2' gin index
        CREATE INDEX property_address_line_2_gin_idx ON property USING GIN (to_tsvector('english', address_line_2));
    '''
    _execute_query(query)
    print('GIN indexes created')


@manager.command
def refresh_gin_indexes():
    """
    Recreate property GIN indexes
    """
    drop_gin_indexes()
    create_gin_indexes()
