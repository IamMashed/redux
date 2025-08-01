"""add payment_status to client

Revision ID: 41ca8828a225
Revises: ce0664de2e2d
Create Date: 2020-07-23 11:45:25.470902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41ca8828a225'
down_revision = 'ce0664de2e2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('case_client', sa.Column('payment_status_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_case_client_payment_status_id', 'case_client', 'case_payment_status',
                          ['payment_status_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_case_client_payment_status_id', 'case_client', type_='foreignkey')
    op.drop_column('case_client', 'payment_status_id')
    # ### end Alembic commands ###
