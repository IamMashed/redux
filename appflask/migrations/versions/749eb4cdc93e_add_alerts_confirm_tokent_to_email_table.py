"""add alerts, confirm_tokent to email table

Revision ID: 749eb4cdc93e
Revises: 82a758f017e5
Create Date: 2020-07-25 22:42:45.544534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '749eb4cdc93e'
down_revision = '82a758f017e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('case_email', sa.Column('alerts', sa.Boolean(), nullable=True))
    op.add_column('case_email', sa.Column('confirm_token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('case_email', 'confirm_token')
    op.drop_column('case_email', 'alerts')
    # ### end Alembic commands ###
