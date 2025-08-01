"""cma task complete ts

Revision ID: 58b48d4148fc
Revises: 19a96f7aff94
Create Date: 2020-02-19 00:29:07.723429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19a96f7aff94'
down_revision = 'ff1704f6f698'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cma_task', sa.Column('task_complete_ts', sa.DateTime(), nullable=True))
    op.add_column('cma_task', sa.Column('total', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cma_task', 'total')
    op.drop_column('cma_task', 'task_complete_ts')
    # pass
    # ### end Alembic commands ###
