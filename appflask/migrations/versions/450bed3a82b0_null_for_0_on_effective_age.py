"""null for 0 on effective_age

Revision ID: 450bed3a82b0
Revises: c536c74959ef
Create Date: 2020-10-28 01:28:00.823402

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '450bed3a82b0'
down_revision = 'c536c74959ef'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        '''
        
        UPDATE property
        SET age = NULL
        WHERE age = 0
          AND county IN ('broward', 'miamidade');
        
        UPDATE property
        SET effective_age = NULL
        WHERE effective_age = 0
          AND county IN ('broward', 'miamidade');
        '''
    )


def downgrade():
    pass
