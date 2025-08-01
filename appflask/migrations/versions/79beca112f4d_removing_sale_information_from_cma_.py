"""removing sale information from cma_result

Revision ID: 79beca112f4d
Revises: 237998ed1d42
Create Date: 2019-12-22 19:13:17.437556

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '79beca112f4d'
down_revision = '237998ed1d42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cma_result', 'sale_price')
    op.drop_column('cma_result', 'sale_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cma_result', sa.Column('sale_date', sa.DATE(), autoincrement=False, nullable=True))
    op.add_column('cma_result', sa.Column('sale_price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
