"""round Florida lot_size to 4 digits

Revision ID: 006d3a559b49
Revises: 058e626c1edf
Create Date: 2020-03-19 17:46:41.009203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006d3a559b49'
down_revision = '058e626c1edf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        UPDATE property
        SET
            lot_size = ROUND(lot_size::numeric, 4)
        WHERE lot_size IS NOT NULL
        AND
            county IN ('broward', 'palmbeach', 'miamidade');        
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
