"""email bad for client

Revision ID: 953ecd8542b0
Revises: 446e8ae79710
Create Date: 2020-07-23 04:52:57.417002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '953ecd8542b0'
down_revision = '446e8ae79710'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('case_client', sa.Column('email_bad', sa.Boolean(), nullable=True))
    op.add_column('case_note', sa.Column('details', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('case_note', 'details')
    op.drop_column('case_client', 'email_bad')
    # ### end Alembic commands ###
