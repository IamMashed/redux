"""add more case application types

Revision ID: ce3f5f379938
Revises: bb723440a0e0
Create Date: 2020-06-11 01:53:18.317276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce3f5f379938'
down_revision = 'bb723440a0e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        UPDATE case_application_type SET name='new_homeowner' WHERE id = 1;

        INSERT INTO case_application_type (id, name, description) 
        VALUES (4, 'misspelled_in_county_records', 'misspelled_in_county_records');

        INSERT INTO case_application_type (id, name, description) 
        VALUES (5, 'co_owner', 'co_owner');

        INSERT INTO case_application_type (id, name, description) 
        VALUES (6, 'authorized_signor', 'authorized_signor');
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        UPDATE case_application_type SET name='new_home_owner' WHERE id = 1;
        DELETE FROM case_application_type WHERE id in (4, 5, 6)
        '''
    )
    # ### end Alembic commands ###
