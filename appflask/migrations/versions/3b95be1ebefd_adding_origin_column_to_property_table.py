"""adding origin column to property table

Revision ID: 3b95be1ebefd
Revises: e22ed27ea2e6
Create Date: 2020-04-18 18:14:35.420023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b95be1ebefd'
down_revision = 'e22ed27ea2e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('property', sa.Column('origin', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('property', 'origin')
    # ### end Alembic commands ###
