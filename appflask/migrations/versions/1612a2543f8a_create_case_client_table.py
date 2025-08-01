"""create case_client table

Revision ID: 1612a2543f8a
Revises: e22ed27ea2e6
Create Date: 2020-04-17 18:39:30.761572

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1612a2543f8a'
down_revision = 'e22ed27ea2e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('case_client',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('tax_year', sa.Integer(), nullable=True),
                    sa.Column('first_name', sa.String(), nullable=True),
                    sa.Column('last_name', sa.String(), nullable=True),
                    sa.Column('mailing_address', sa.String(), nullable=True),
                    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=True),
                    sa.Column('default_fee', sa.Integer(), nullable=True),
                    sa.Column('marketing_code', sa.String(), nullable=True),
                    sa.Column('_phone_number', sa.Unicode(length=20), nullable=True),
                    sa.Column('country_code', sa.Unicode(length=8), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('case_client')
    # ### end Alembic commands ###
