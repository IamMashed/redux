"""add settled_amount to billing

Revision ID: 7907b03f60ff
Revises: fb3c1aa60682
Create Date: 2020-07-23 13:24:57.182930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7907b03f60ff'
down_revision = 'fb3c1aa60682'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('case_billing', sa.Column('settled_amount', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('case_billing', 'settled_amount')
    # ### end Alembic commands ###
