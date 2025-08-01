"""assessment date name nullable

Revision ID: 5400f5bfc400
Revises: 50d400266dc1
Create Date: 2020-03-06 17:54:30.347424

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5400f5bfc400'
down_revision = '50d400266dc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('assessment_dates', 'name',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
