"""adding origin column to property_original

Revision ID: d90e2da58f05
Revises: 3b95be1ebefd
Create Date: 2020-04-21 15:35:35.904130

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd90e2da58f05'
down_revision = '3b95be1ebefd'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('''
    alter table property_original
	add origin varchar;
    ''')


def downgrade():
    pass
