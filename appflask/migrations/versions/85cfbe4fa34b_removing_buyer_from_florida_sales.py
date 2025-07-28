"""removing buyer from florida sales

Revision ID: 85cfbe4fa34b
Revises: 440e02ff3506
Create Date: 2020-04-22 17:59:04.225542

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '85cfbe4fa34b'
down_revision = '440e02ff3506'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('''
    
    UPDATE sale
    SET buyer_first_name = NULL,
        buyer_last_name  = NULL
    FROM property
    WHERE sale.property_id = property.id
      AND property.county IN ('broward', 'palmbeach', 'miamidade')
    
    ''')


def downgrade():
    pass
