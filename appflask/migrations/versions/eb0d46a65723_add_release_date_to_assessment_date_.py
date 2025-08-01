"""add release_date to assessment_date table

Revision ID: eb0d46a65723
Revises: 27d3f7f4bfaf
Create Date: 2020-07-14 03:36:45.875697

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'eb0d46a65723'
down_revision = '27d3f7f4bfaf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assessment_dates', sa.Column('release_date', sa.Date(), nullable=True))

    op.execute(
        '''
        UPDATE assessment_dates
        SET release_date='2020-07-01'
        WHERE id in (8, 10);
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('assessment_dates', 'release_date')
    # ### end Alembic commands ###
