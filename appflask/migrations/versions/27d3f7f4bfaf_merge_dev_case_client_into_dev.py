"""merge dev-case-client into dev

Revision ID: 27d3f7f4bfaf
Revises: eaf47f32f00b, 8855e1cc8230
Create Date: 2020-07-14 01:26:12.486356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27d3f7f4bfaf'
down_revision = ('eaf47f32f00b', '8855e1cc8230')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
