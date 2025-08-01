"""land_use index to property

Revision ID: 1ceeea043645
Revises: a1b992184ee7
Create Date: 2020-05-13 00:10:30.785061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ceeea043645'
down_revision = 'a1b992184ee7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_property_land_use'), 'property', ['land_use'], unique=False)
    op.create_index(op.f('ix_property_original_land_use'), 'property_original', ['land_use'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_property_original_land_use'), table_name='property_original')
    op.drop_index(op.f('ix_property_land_use'), table_name='property')
    # ### end Alembic commands ###
