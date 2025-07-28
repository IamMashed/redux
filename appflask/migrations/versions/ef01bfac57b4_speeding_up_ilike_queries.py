"""speeding up ilike queries

Revision ID: ef01bfac57b4
Revises: 4e64e1d3c91d
Create Date: 2020-10-14 21:51:08.612021

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ef01bfac57b4'
down_revision = '4e64e1d3c91d'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('''

    CREATE EXTENSION pg_trgm;

    CREATE INDEX property_apn_gin_trgm_idx ON property USING gin (apn gin_trgm_ops);

    CREATE INDEX property_id_gin_trgm_idx on property using gin (cast(id as varchar) gin_trgm_ops);


    ''')
    pass


def downgrade():
    op.execute('''
        
        
    DROP INDEX property_apn_gin_trgm_idx;
    DROP INDEX property_id_gin_trgm_idx;
    DROP EXTENSION pg_trgm;
        
    
    ''')
