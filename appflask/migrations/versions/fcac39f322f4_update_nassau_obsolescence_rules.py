"""update nassau obsolescence rules

Revision ID: fcac39f322f4
Revises: 817114474a37
Create Date: 2020-12-15 03:57:36.888480

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fcac39f322f4'
down_revision = '817114474a37'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('''
    UPDATE properties_rules
    SET obsolescence_rules = '{0.000,5.000,5.000,5.000,5.000,3.000,3.000,10.000,5.000,0.000,5.000,3.000,10.000,7.000,5.000,10.000,3.000,5.000,5.000,5.000,5.000,5.000,0.000,5.000,3.000,3.000,5.000,3.000,3.000,5.000,7.000,10.000,5.000,10.000,5.000,5.000,5.000,5.000,5.000,5.000,5.000,5.000,5.000,5.000,5.000,5.000,5.000,5.000,5.000}'
    WHERE county = 'nassau'
    ''')


def downgrade():
    pass
