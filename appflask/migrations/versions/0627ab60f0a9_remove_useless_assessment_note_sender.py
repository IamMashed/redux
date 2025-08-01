"""remove useless Assessment note sender

Revision ID: 0627ab60f0a9
Revises: fb6e60471d73
Create Date: 2020-07-25 03:14:25.854302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0627ab60f0a9'
down_revision = 'fb6e60471d73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        DELETE FROM case_note_sender WHERE id=4;
        UPDATE case_note_sender SET name='Case Property' WHERE id=3;
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        INSERT INTO case_note_sender (id, name) VALUES (4, 'Assessment');
        UPDATE case_note_sender SET name='Property' WHERE id=3;
        '''
    )
    # ### end Alembic commands ###
