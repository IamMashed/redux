"""fix nassau, suffolk town names

Revision ID: f7aa928fbac1
Revises: 535145082ebf
Create Date: 2020-06-18 01:33:53.857173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7aa928fbac1'
down_revision = '535145082ebf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # nassau
    op.execute(
        '''
        update property set town='Hempstead' where town='1' and county='nassau';
        update property set town='North Hempstead' where town='2' and county='nassau';
        update property set town='Oyster Bay' where town='3' and county='nassau';
        update property set town='Glen Cove' where town='4' and county='nassau';
        update property set town='Long Beach' where town='5' and county='nassau';
        '''
    )

    # suffolk
    op.execute(
        '''
        update property set town='Babylon' where town='100' and county='suffolk';
        update property set town='Brookhaven' where town='200' and county='suffolk';
        update property set town='East Hampton' where town='300' and county='suffolk';
        update property set town='Hungtington' where town='400' and county='suffolk';
        update property set town='Islip' where town='500' and county='suffolk';
        update property set town='Riverhead' where town='600' and county='suffolk';
        update property set town='Shelter Island' where town='700' and county='suffolk';
        update property set town='Smithtown' where town='800' and county='suffolk';
        update property set town='Southampton' where town='900' and county='suffolk';
        update property set town='Southold' where town='1000' and county='suffolk';
        '''
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # nassau
    op.execute(
        '''
        update property set town='1' where town='Hempstead' and county='nassau';
        update property set town='2' where town='North Hempstead' and county='nassau';
        update property set town='3' where town='Oyster Bay' and county='nassau';
        update property set town='4' where town='Glen Cove' and county='nassau';
        update property set town='5' where town='Long Beach' and county='nassau';
        '''
    )

    # suffolk
    op.execute(
        '''
        update property set town='100' where town='Babylon' and county='suffolk';
        update property set town='200' where town='Brookhaven' and county='suffolk';
        update property set town='300' where town='East Hampton' and county='suffolk';
        update property set town='400' where town='Hungtington' and county='suffolk';
        update property set town='500' where town='Islip' and county='suffolk';
        update property set town='600' where town='Riverhead' and county='suffolk';
        update property set town='700' where town='Shelter Island' and county='suffolk';
        update property set town='800' where town='Smithtown' and county='suffolk';
        update property set town='900' where town='Southampton' and county='suffolk';
        update property set town='1000' where town='Southold' and county='suffolk';
        '''
    )

    # ### end Alembic commands ###
