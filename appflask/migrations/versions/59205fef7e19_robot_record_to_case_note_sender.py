"""robot record to case note sender

Revision ID: 59205fef7e19
Revises: 0f809802ce0c
Create Date: 2020-08-19 18:58:19.181491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59205fef7e19'
down_revision = '0f809802ce0c'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('''
    INSERT INTO case_note_sender (id, name)
    VALUES (5, 'Robot')
    ''')

def downgrade():
    pass