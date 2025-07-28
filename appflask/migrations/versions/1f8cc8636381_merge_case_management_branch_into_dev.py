"""merge case-management branch into dev

Revision ID: 1f8cc8636381
Revises: 137eb853cab3, e95899f379d2
Create Date: 2020-06-02 19:19:16.983510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f8cc8636381'
down_revision = ('137eb853cab3', 'e95899f379d2')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
