"""merge dev-hearing-date into dev

Revision ID: 4b8c941d6481
Revises: ef01bfac57b4, 538d44f6b009
Create Date: 2020-10-15 00:28:44.411950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b8c941d6481'
down_revision = ('ef01bfac57b4', '538d44f6b009')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
