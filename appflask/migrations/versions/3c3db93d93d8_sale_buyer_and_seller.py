"""sale buyer and seller

Revision ID: 3c3db93d93d8
Revises: d90e2da58f05
Create Date: 2020-04-21 23:26:11.386827

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3c3db93d93d8'
down_revision = 'd90e2da58f05'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('''
    
        UPDATE sale
        SET buyer_first_name = first_name,
            buyer_last_name=last_name
        FROM owner,
             property
        WHERE owner.property_id = property.id
          and sale.property_id = property.id
          AND sale.arms_length = TRUE
          AND buyer_first_name IS NULL
          AND buyer_last_name IS NULL
          AND owner.data_source = 'property'
    ''')


def downgrade():
    op.execute('''
    
        UPDATE sale
        SET buyer_first_name = NULL,
            buyer_last_name  = NULL
        FROM property
        WHERE sale.property_id = property.id
        AND property.county IN ('broward', 'palmbeach', 'miamidade')
    
    ''')
