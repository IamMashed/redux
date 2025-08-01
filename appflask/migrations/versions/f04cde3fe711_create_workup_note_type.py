"""create workup note type

Revision ID: f04cde3fe711
Revises: edbe5b24c0ea
Create Date: 2020-10-16 00:11:23.292521

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f04cde3fe711'
down_revision = 'edbe5b24c0ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        INSERT INTO case_note_type (id, name, action) VALUES (14, 'System', 'workup_created');
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        DELETE FROM case_note WHERE type_id=14;
        DELETE FROM case_note_type WHERE id=14;
        '''
    )
    # ### end Alembic commands ###
