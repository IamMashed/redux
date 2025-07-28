"""merge dev-activity-log-capture-changes into dev

Revision ID: fae5b2737f78
Revises: 168bb727c797, 17bb399f480a
Create Date: 2020-07-23 23:39:37.375102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fae5b2737f78'
down_revision = ('168bb727c797', '17bb399f480a')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
