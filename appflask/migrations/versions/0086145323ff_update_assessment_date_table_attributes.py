"""update assessment_date table attributes

Revision ID: 0086145323ff
Revises: ad87e3e01fed
Create Date: 2020-03-10 02:17:10.834070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0086145323ff'
down_revision = 'ad87e3e01fed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assessment_dates', sa.Column('assessment_name', sa.String(), nullable=True))
    op.drop_column('assessment_dates', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assessment_dates', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('assessment_dates', 'assessment_name')
    # ### end Alembic commands ###
