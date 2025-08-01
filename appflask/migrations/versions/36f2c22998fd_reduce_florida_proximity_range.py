"""reduce Florida proximity range

Revision ID: 36f2c22998fd
Revises: 8cf8814baa0a
Create Date: 2020-03-14 23:25:01.737874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36f2c22998fd'
down_revision = '8cf8814baa0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        update selection_rules
        set proximity_range = 2.0
        where id in (2, 3, 4)
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        update selection_rules
        set proximity_range = 30.0
        where id in (2, 3, 4)
        '''
    )
    # ### end Alembic commands ###
