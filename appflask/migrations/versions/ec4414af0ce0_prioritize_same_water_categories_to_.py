"""prioritize_same_water_categories to selection rules

Revision ID: ec4414af0ce0
Revises: 133fa46d233e
Create Date: 2020-06-26 19:59:02.349195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec4414af0ce0'
down_revision = '133fa46d233e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('selection_rules', sa.Column('prioritize_same_water_categories', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('selection_rules', 'prioritize_same_water_categories')
    # ### end Alembic commands ###
