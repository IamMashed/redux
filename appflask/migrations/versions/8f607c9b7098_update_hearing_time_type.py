"""update hearing_time type

Revision ID: 8f607c9b7098
Revises: 4e64e1d3c91d
Create Date: 2020-10-14 20:54:13.153373

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8f607c9b7098'
down_revision = '4e64e1d3c91d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('case_property', 'hearing_time',
                    existing_type=postgresql.TIMESTAMP(),
                    type_=sa.Time(),
                    existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('case_property', 'hearing_time',
                    existing_type=sa.Time(),
                    type_=postgresql.TIMESTAMP(),
                    existing_nullable=True)
    # ### end Alembic commands ###
