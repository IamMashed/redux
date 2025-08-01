"""email as unique case_client constraint

Revision ID: f2c707a96efd
Revises: 22b9472e7173
Create Date: 2020-05-13 20:00:01.948445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2c707a96efd'
down_revision = '22b9472e7173'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uc_CaseApplication_first_name_last_name_email', 'case_application', type_='unique')
    op.create_unique_constraint('uc_CaseClient_email', 'case_client', ['email'])
    op.drop_constraint('uc_CaseClient_first_name_last_name_email', 'case_client', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uc_CaseClient_first_name_last_name_email', 'case_client',
                                ['first_name', 'last_name', 'email'])
    op.drop_constraint('uc_CaseClient_email', 'case_client', type_='unique')
    op.create_unique_constraint('uc_CaseApplication_first_name_last_name_email', 'case_application',
                                ['first_name', 'last_name', 'email'])
    # ### end Alembic commands ###
