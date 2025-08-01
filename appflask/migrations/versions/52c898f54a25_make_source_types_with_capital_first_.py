"""make source types with capital first letter in case_application_source table

Revision ID: 52c898f54a25
Revises: ec4414af0ce0
Create Date: 2020-06-29 12:26:13.388068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52c898f54a25'
down_revision = 'ec4414af0ce0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        UPDATE case_application_source
        SET name='Physical'
        WHERE id=1;
        
        UPDATE case_application_source
        SET name='Digital'
        WHERE id=2;
        
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        UPDATE case_application_source
        SET name='physical'
        WHERE id=1;

        UPDATE case_application_source
        SET name='digital'
        WHERE id=2;

        '''
    )
    # ### end Alembic commands ###
