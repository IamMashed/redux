"""add petition_number, hearing_date, hearing_time, board_room to case

Revision ID: c549677e3135
Revises: a1bebecbea53
Create Date: 2020-10-03 23:11:03.189917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c549677e3135'
down_revision = 'a1bebecbea53'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('case_property', sa.Column('board_room', sa.String(), nullable=True))
    op.add_column('case_property', sa.Column('hearing_date', sa.DateTime(), nullable=True))
    op.add_column('case_property', sa.Column('hearing_time', sa.DateTime(), nullable=True))
    op.add_column('case_property', sa.Column('petition_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('case_property', 'petition_number')
    op.drop_column('case_property', 'hearing_time')
    op.drop_column('case_property', 'hearing_date')
    op.drop_column('case_property', 'board_room')
    # ### end Alembic commands ###
