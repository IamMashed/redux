"""add system note sub types to case_note_note table

Revision ID: da40ae42f365
Revises: 343fe52ed8b4
Create Date: 2020-05-25 15:47:22.181294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da40ae42f365'
down_revision = '343fe52ed8b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('case_note_type', sa.Column('action', sa.String(), nullable=True))

    op.execute(
        '''
        UPDATE case_note_type SET action='submitted' WHERE id = 1;
        INSERT INTO case_note_type (id, name, action) VALUES (3, 'System', 'approved');
        INSERT INTO case_note_type (id, name, action) VALUES (4, 'System', 'rejected');
        '''
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        DELETE FROM case_note_type WHERE id IN (3, 4);
        '''
    )
    op.drop_column('case_note_type', 'action')

    # ### end Alembic commands ###
