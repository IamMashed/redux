"""add assigned_to attribute in case_application table

Revision ID: be8260a7b4e3
Revises: 4237a1c8d039
Create Date: 2020-05-02 22:34:47.619470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be8260a7b4e3'
down_revision = '4237a1c8d039'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('case_application', sa.Column('assigned_to', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_CaseApplication_assigned_to', 'case_application', 'users', ['assigned_to'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_CaseApplication_assigned_to', 'case_application', type_='foreignkey')
    op.drop_column('case_application', 'assigned_to')
    # ### end Alembic commands ###
