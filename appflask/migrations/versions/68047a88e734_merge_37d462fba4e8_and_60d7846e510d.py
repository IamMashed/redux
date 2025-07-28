"""merge 37d462fba4e8 and 60d7846e510d

Revision ID: 68047a88e734
Revises: 37d462fba4e8, 60d7846e510d
Create Date: 2020-01-16 04:11:39.103272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68047a88e734'
down_revision = ('37d462fba4e8', '60d7846e510d')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
