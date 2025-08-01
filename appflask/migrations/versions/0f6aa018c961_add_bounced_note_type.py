"""add bounced note type

Revision ID: 0f6aa018c961
Revises: 404ccbc3864a
Create Date: 2020-07-29 19:02:01.359253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f6aa018c961'
down_revision = '404ccbc3864a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        INSERT INTO case_note_type (id, name, action) VALUES (8, 'System', 'bounced');
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        DELETE FROM case_note_type WHERE id=8;
        '''
    )
    # ### end Alembic commands ###
