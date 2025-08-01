"""add property_inventories_override table

Revision ID: 1452930dcbad
Revises: 006d3a559b49
Create Date: 2020-03-20 20:31:10.960746

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1452930dcbad'
down_revision = '006d3a559b49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('property_inventories_override',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('property_id', sa.Integer(), nullable=False),
                    sa.Column('gla_sqft', sa.Float(), nullable=True),
                    sa.Column('lot_size', sa.Float(), nullable=True),
                    sa.Column('full_baths', sa.Integer(), nullable=True),
                    sa.Column('half_baths', sa.Integer(), nullable=True),
                    sa.Column('bedrooms', sa.Integer(), nullable=True),
                    sa.Column('patio_type', sa.Integer(), nullable=True),
                    sa.Column('porch_type', sa.Integer(), nullable=True),
                    sa.Column('pool', sa.Boolean(), nullable=True),
                    sa.Column('paving_type', sa.Integer(), nullable=True),
                    sa.Column('garages', sa.Integer(), nullable=True),
                    sa.Column('basement_type', sa.Integer(), nullable=True),
                    sa.Column('heat_type', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['property_id'], ['property.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('property_inventories_override')
    # ### end Alembic commands ###
