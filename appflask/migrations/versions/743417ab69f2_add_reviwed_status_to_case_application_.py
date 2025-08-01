"""add reviwed status to case_application_status

Revision ID: 743417ab69f2
Revises: 7907b03f60ff
Create Date: 2020-07-23 17:20:46.427572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '743417ab69f2'
down_revision = '7907b03f60ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        INSERT INTO case_application_status (id, name) VALUES (5, 'Reviewed');
        
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        DELETE FROM case_application_status WHERE id=5;
        '''
    )
    # ### end Alembic commands ###
