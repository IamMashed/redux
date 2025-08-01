"""add override market value to assessment table

Revision ID: ebc3d89721c0
Revises: e24fa420a5d6
Create Date: 2020-12-04 02:34:19.938459

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ebc3d89721c0'
down_revision = 'e24fa420a5d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assessment', sa.Column('market_value_override', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('assessment', 'market_value_override')
    # ### end Alembic commands ###
