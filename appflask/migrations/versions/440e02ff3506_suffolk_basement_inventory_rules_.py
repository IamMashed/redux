"""suffolk basement inventory rules adjusted

Revision ID: 440e02ff3506
Revises: 3c3db93d93d8
Create Date: 2020-04-22 16:27:43.516207

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '440e02ff3506'
down_revision = '3c3db93d93d8'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('''
    
    UPDATE public.inventory_rules
    SET basement_prices = '{0,7500,15000,22500,30000,0,0,0}'
    WHERE id = 23;
    UPDATE public.inventory_rules
    SET basement_prices = '{0,1250,2500,3750,5000,0,0,0}'
    WHERE id = 26;
    UPDATE public.inventory_rules
    SET basement_prices = '{0,5000,10000,15000,20000,0,0,0}'
    WHERE id = 24;
    UPDATE public.inventory_rules
    SET basement_prices = '{0,10000,20000,30000,40000,0,0,0}'
    WHERE id = 22;
    UPDATE public.inventory_rules
    SET basement_prices = '{0,2500,5000,7500,10000,0,0,0}'
    WHERE id = 25;
    
    ''')


def downgrade():
    pass
