"""modify application foreign key attributes

Revision ID: 68410d6f3d64
Revises: e9ea6f0fedbf
Create Date: 2020-05-19 17:22:09.803085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68410d6f3d64'
down_revision = 'e9ea6f0fedbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_case_application_company_id', 'case_application', type_='foreignkey')
    op.drop_constraint('fk_case_application_case_property_id', 'case_application', type_='foreignkey')
    op.drop_constraint('fk_case_application_property_id', 'case_application', type_='foreignkey')
    op.drop_constraint('fk_case_application_status_id', 'case_application', type_='foreignkey')
    op.create_foreign_key('fk_case_application_case_property_id', 'case_application', 'case_property',
                          ['case_property_id'], ['id'])
    op.create_foreign_key('fk_case_application_property_id', 'case_application', 'property', ['property_id'], ['id'])
    op.create_foreign_key('fk_case_application_status_id', 'case_application', 'case_application_status', ['status_id'], ['id'])
    op.create_foreign_key('fk_case_application_company_id', 'case_application', 'case_company_serving', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_case_application_company_id', 'case_application', type_='foreignkey')
    op.drop_constraint('fk_case_application_status_id', 'case_application', type_='foreignkey')
    op.drop_constraint('fk_case_application_property_id', 'case_application', type_='foreignkey')
    op.drop_constraint('fk_case_application_case_property_id', 'case_application', type_='foreignkey')
    op.create_foreign_key('fk_case_application_status_id', 'case_application', 'case_application_status',
                          ['status_id'], ['id'], onupdate='CASCADE')
    op.create_foreign_key('fk_case_application_property_id', 'case_application', 'property', ['property_id'], ['id'],
                          onupdate='CASCADE')
    op.create_foreign_key('fk_case_application_case_property_id', 'case_application', 'case_property',
                          ['case_property_id'], ['id'], onupdate='CASCADE')
    op.create_foreign_key('fk_case_application_company_id', 'case_application', 'case_company_serving',
                          ['company_id'], ['id'], onupdate='CASCADE')
    # ### end Alembic commands ###
