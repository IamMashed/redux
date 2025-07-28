"""merge dev into dev-migrate-payment

Revision ID: 2b3517aa15cc
Revises: df29b1fb4821, 250aecfa5298
Create Date: 2020-08-01 15:00:29.207082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b3517aa15cc'
down_revision = ('df29b1fb4821', '250aecfa5298')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
