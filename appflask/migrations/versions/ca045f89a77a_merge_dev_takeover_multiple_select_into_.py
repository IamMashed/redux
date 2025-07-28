"""merge dev-takeover-multiple-select into dev

Revision ID: ca045f89a77a
Revises: ad37dc58c9d2, 2b5231588696
Create Date: 2020-07-20 11:09:03.705983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca045f89a77a'
down_revision = ('ad37dc58c9d2', '2b5231588696')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
