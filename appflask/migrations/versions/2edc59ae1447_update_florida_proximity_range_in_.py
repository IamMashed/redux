"""update florida proximity range in selection rules table

Revision ID: 2edc59ae1447
Revises: 5896f85f2e2e
Create Date: 2020-03-06 02:07:18.336677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2edc59ae1447'
down_revision = '5896f85f2e2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        update selection_rules
        set proximity_range = 30.0
        where parent_id in (43, 52, 62);
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
