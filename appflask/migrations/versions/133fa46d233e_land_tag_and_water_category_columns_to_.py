"""land_tag and water_category columns to property table

Revision ID: 133fa46d233e
Revises: 59e3f68e475a
Create Date: 2020-06-25 19:20:42.012706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '133fa46d233e'
down_revision = '59e3f68e475a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('property', sa.Column('land_tag', sa.Integer(), nullable=True))
    op.add_column('property', sa.Column('water_category', sa.Integer(), nullable=True))
    op.add_column('property_original', sa.Column('land_tag', sa.Integer(), nullable=True))
    op.add_column('property_original', sa.Column('water_category', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('property_original', 'water_category')
    op.drop_column('property_original', 'land_tag')
    op.drop_column('property', 'water_category')
    op.drop_column('property', 'land_tag')
    # ### end Alembic commands ###
