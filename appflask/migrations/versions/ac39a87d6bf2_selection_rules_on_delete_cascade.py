"""selection rules on delete cascade

Revision ID: ac39a87d6bf2
Revises: 1c02cd914977
Create Date: 2020-01-21 19:51:28.606417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac39a87d6bf2'
down_revision = '1c02cd914977'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('selection_rules_parent_id_fkey', 'selection_rules', type_='foreignkey')
    op.create_foreign_key('selection_rules_parent_id_fkey', 'selection_rules', 'properties_rules', ['parent_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('selection_rules_parent_id_fkey', 'selection_rules', type_='foreignkey')
    op.create_foreign_key('selection_rules_parent_id_fkey', 'selection_rules', 'properties_rules', ['parent_id'], ['id'])
    # ### end Alembic commands ###
