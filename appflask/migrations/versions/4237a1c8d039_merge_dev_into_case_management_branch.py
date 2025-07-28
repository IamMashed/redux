"""merge dev into case_management branch

Revision ID: 4237a1c8d039
Revises: 339072537168, 7ce2578d5998
Create Date: 2020-05-02 20:42:31.639688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4237a1c8d039'
down_revision = ('339072537168', '7ce2578d5998')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
