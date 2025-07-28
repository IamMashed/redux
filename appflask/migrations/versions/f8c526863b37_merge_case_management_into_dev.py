"""merge case-management into dev

Revision ID: f8c526863b37
Revises: fad191763141, 23fb837495a6
Create Date: 2020-05-22 17:41:43.208530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8c526863b37'
down_revision = ('fad191763141', '23fb837495a6')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
