"""fix nassau assessments

Revision ID: caba32a41a3f
Revises: da141728b2a4
Create Date: 2020-12-15 02:49:11.488194

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'caba32a41a3f'
down_revision = 'da141728b2a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        -- fix assessment files
        UPDATE assessment_files
        SET assessment_date_id=9
        WHERE assessment_date_id=6;

        -- fix assessment dates        
        UPDATE assessment_dates
        SET assessment_name = (SELECT assessment_name FROM assessment_dates WHERE id = 6)
        WHERE id = 9;

        -- delete duplicates
        DELETE FROM assessment
        WHERE assessment_id = 6;
        
        DELETE FROM assessment_dates 
        WHERE id = 6;
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
