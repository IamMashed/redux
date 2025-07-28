"""merge dev-application-repair to dev

Revision ID: 926d4a79ae8b
Revises: dbf12d63549f, 12e83ddfb0c7
Create Date: 2020-08-02 14:07:22.807336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '926d4a79ae8b'
down_revision = ('dbf12d63549f', '12e83ddfb0c7')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
