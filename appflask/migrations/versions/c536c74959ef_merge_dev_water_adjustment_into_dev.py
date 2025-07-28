"""merge dev-water-adjustment into dev

Revision ID: c536c74959ef
Revises: ae133d3ab7fd, 030a49ec57ad
Create Date: 2020-10-27 22:18:33.930306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c536c74959ef'
down_revision = ('ae133d3ab7fd', '030a49ec57ad')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
