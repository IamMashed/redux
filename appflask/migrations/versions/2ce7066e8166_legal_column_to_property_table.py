"""legal column to property table

Revision ID: 2ce7066e8166
Revises: b72714d11a43
Create Date: 2020-09-16 17:09:54.717796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ce7066e8166'
down_revision = 'b72714d11a43'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('property', sa.Column('legal', sa.String(), nullable=True))
    op.add_column('property_original', sa.Column('legal', sa.String(), nullable=True))


def downgrade():
    op.drop_column('property', 'legal')
    op.drop_column('property_original', 'legal')

