"""rename duplicate nassau village name NP to NPH

Revision ID: 3f16fc5bca94
Revises: cc7928fa6bad
Create Date: 2020-04-13 18:25:07.291458

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '3f16fc5bca94'
down_revision = 'cc7928fa6bad'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('''
    update property 
    set village = 'NHP'
    where village = 'NP' and county='nassau'
    ''')


def downgrade():
    pass
