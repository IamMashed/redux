"""renaming checkinvoice table

Revision ID: 998eb2f5d72f
Revises: 59205fef7e19
Create Date: 2020-08-24 16:44:55.124733

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '998eb2f5d72f'
down_revision = '59205fef7e19'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('''
    ALTER TABLE case_check_payment_invoice RENAME TO case_payment_invoice;

    ''')


def downgrade():
    pass
