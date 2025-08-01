"""update values for fireplaces of nassau inventory rules

Revision ID: aca82cfa04ce
Revises: 6abffafc627c
Create Date: 2020-05-21 01:23:43.309847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aca82cfa04ce'
down_revision = '6abffafc627c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('''
    update inventory_rules set fireplace = 1000 where id = 6;
    update inventory_rules set fireplace = 1500 where id = 5;
    update inventory_rules set fireplace = 2000 where id = 4;
    update inventory_rules set fireplace = 2500 where id = 3;
    update inventory_rules set fireplace = 3000 where id = 2;
    
    update properties_rules set adjustments_all = '{GLA,LOT,FULL_BATH,HALF_BATH,GARAGE,BASEMENT,TIME_ADJ,LOCATION,FIREPLACE}' where id in (57,42);
    update properties_rules set adjustments_all = '{GLA,LOT,FULL_BATH,HALF_BATH,GARAGE,BASEMENT,FIREPLACE}' where id = 39;
    ''')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
