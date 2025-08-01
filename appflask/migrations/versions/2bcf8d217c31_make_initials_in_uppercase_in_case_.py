"""make initials in uppercase in case_application table

Revision ID: 2bcf8d217c31
Revises: 971349c9e120
Create Date: 2020-06-29 12:44:44.675143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bcf8d217c31'
down_revision = '971349c9e120'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        UPDATE case_application
        SET initials = UPPER(initials)
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
