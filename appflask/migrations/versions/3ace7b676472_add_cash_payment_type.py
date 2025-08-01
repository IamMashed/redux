"""add cash payment type

Revision ID: 3ace7b676472
Revises: a584e7448698
Create Date: 2020-07-25 00:06:23.155316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ace7b676472'
down_revision = 'a584e7448698'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        INSERT INTO case_payment_type (id, name, description) VALUES (3, 'cash', 'Cash');
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        DELETE FROM case_payment_type WHERE id = 3;
        '''
    )
    # ### end Alembic commands ###
