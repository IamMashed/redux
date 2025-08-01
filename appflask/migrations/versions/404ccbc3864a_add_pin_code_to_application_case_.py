"""add pin_code to application, case property

Revision ID: 404ccbc3864a
Revises: 0a22fbe2d57f
Create Date: 2020-07-29 01:47:32.077977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '404ccbc3864a'
down_revision = '0a22fbe2d57f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('case_application', sa.Column('pin_code', sa.String(), nullable=True))
    op.add_column('case_property', sa.Column('pin_code', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('case_property', 'pin_code')
    op.drop_column('case_application', 'pin_code')
    # ### end Alembic commands ###
