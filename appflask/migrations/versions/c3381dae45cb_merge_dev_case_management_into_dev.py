"""merge dev-case-management into dev

Revision ID: c3381dae45cb
Revises: da40ae42f365, 813509ba021a
Create Date: 2020-05-25 19:49:53.283138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3381dae45cb'
down_revision = ('da40ae42f365', '813509ba021a')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
