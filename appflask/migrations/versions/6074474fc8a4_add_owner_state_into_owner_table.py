"""add owner_state into owner table

Revision ID: 6074474fc8a4
Revises: 5a44b28d6bdd
Create Date: 2020-06-01 19:46:06.112105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6074474fc8a4'
down_revision = '5a44b28d6bdd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('owner', sa.Column('owner_state', sa.String(), nullable=True))
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_column('owner', 'owner_state')
    pass
    # ### end Alembic commands ###
