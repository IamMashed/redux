"""add to cmatask assessment_date_id

Revision ID: c32c8a05179a
Revises: 634ec36c9b13
Create Date: 2020-03-19 12:58:40.064928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c32c8a05179a'
down_revision = '634ec36c9b13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cma_task', sa.Column('assessment_date_id', sa.Integer(), nullable=True))
    op.create_foreign_key('cma_task_assessment_dates_id_fkey', 'cma_task', 'assessment_dates', ['assessment_date_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('cma_task_assessment_dates_id_fkey', 'cma_task', type_='foreignkey')
    op.drop_column('cma_task', 'assessment_date_id')
    # ### end Alembic commands ###
