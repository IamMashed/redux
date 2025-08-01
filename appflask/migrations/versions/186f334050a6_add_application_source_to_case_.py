"""add application_source to case_application table

Revision ID: 186f334050a6
Revises: f1ce97e27595
Create Date: 2020-05-11 23:23:16.924088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '186f334050a6'
down_revision = 'f1ce97e27595'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('''
    delete from case_application''')
    op.add_column('case_application', sa.Column('application_source_id', sa.Integer(), nullable=False))
    op.add_column('case_application', sa.Column('scan_encoded', sa.LargeBinary(), nullable=True))
    op.add_column('case_application', sa.Column('signature_encoded', sa.LargeBinary(), nullable=False))
    op.create_foreign_key('fk_CaseApplication_case_application_source_id', 'case_application', 'case_application_source', ['application_source_id'], ['id'])
    op.drop_column('case_application', 'scan')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('case_application', sa.Column('scan', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint('fk_CaseApplication_case_application_source_id', 'case_application', type_='foreignkey')
    op.drop_column('case_application', 'signature_encoded')
    op.drop_column('case_application', 'scan_encoded')
    op.drop_column('case_application', 'application_source_id')
    # ### end Alembic commands ###
