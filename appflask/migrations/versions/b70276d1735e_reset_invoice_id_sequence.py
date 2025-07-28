"""reset invoice id sequence

Revision ID: b70276d1735e
Revises: dad26cdb3516
Create Date: 2020-08-16 12:02:28.263429

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'b70276d1735e'
down_revision = 'dad26cdb3516'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('''
    ALTER SEQUENCE case_check_payment_invoice_id_seq RESTART WITH 2501;
    ''')

def downgrade():
    pass