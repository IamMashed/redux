"""merge case_management into dev

Revision ID: 9a0fa7264520
Revises: c498e5b02364, 6ab3c0dbd4a9
Create Date: 2020-05-11 23:44:22.716960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a0fa7264520'
down_revision = ('c498e5b02364', '6ab3c0dbd4a9')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
