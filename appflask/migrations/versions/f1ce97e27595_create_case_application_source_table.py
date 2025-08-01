"""create case_application_source table

Revision ID: f1ce97e27595
Revises: 9cfbbc9c2e09
Create Date: 2020-05-11 22:58:34.679244

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f1ce97e27595'
down_revision = '9cfbbc9c2e09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('case_application_source',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('type', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('case_application_source')
    # ### end Alembic commands ###
