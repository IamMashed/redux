"""add default value for basement_prices column in inventory_rules table

Revision ID: a409bb4ff432
Revises: 58b48d4148fc
Create Date: 2020-02-19 14:42:41.984934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a409bb4ff432'
down_revision = '58b48d4148fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        ALTER TABLE inventory_rules ALTER COLUMN basement_prices SET DEFAULT '{}';        
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        ALTER TABLE inventory_rules ALTER COLUMN basement_prices SET DEFAULT NULL;               
        '''
    )
    # ### end Alembic commands ###
