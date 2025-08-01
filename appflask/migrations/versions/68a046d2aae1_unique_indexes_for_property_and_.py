"""unique indexes for property and property_original tables

Revision ID: 68a046d2aae1
Revises: 93febfbe02f9
Create Date: 2020-05-09 01:05:24.650280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68a046d2aae1'
down_revision = '93febfbe02f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_Property_address', 'property', ['address'], unique=False)
    op.create_index('ix_Property_another_combined_index', 'property', ['county', 'school_district', 'property_class', 'town', 'street', 'property_style'], unique=False)
    op.create_index('ix_Property_apn', 'property', ['apn'], unique=False)
    op.create_index('ix_Property_block', 'property', ['block'], unique=False)
    op.create_index('ix_Property_county', 'property', ['county'], unique=False)
    op.create_index('ix_Property_lot', 'property', ['lot'], unique=False)
    op.create_index('ix_Property_number', 'property', ['number'], unique=False)
    op.create_index('ix_Property_print_key', 'property', ['print_key'], unique=False)
    op.create_index('ix_Property_school_district', 'property', ['school_district'], unique=False)
    op.create_index('ix_Property_section', 'property', ['section'], unique=False)
    op.create_index('ix_Property_state', 'property', ['state'], unique=False)
    op.create_index('ix_Property_street', 'property', ['street'], unique=False)
    op.create_index('ix_Property_town', 'property', ['town'], unique=False)
    op.create_index('ix_Property_undefined_field', 'property', ['undefined_field'], unique=False)
    op.create_index('ix_Property_village', 'property', ['village'], unique=False)
    op.create_index('ix_Property_zip', 'property', ['zip'], unique=False)
    op.create_unique_constraint('uc_Property_apn_county', 'property', ['apn', 'county'])
    op.drop_constraint('_apn_county_uc', 'property', type_='unique')
    op.create_index('ix_PropertyOriginal_address', 'property_original', ['address'], unique=False)
    op.create_index('ix_PropertyOriginal_another_combined_index', 'property_original', ['county', 'school_district', 'property_class', 'town', 'street', 'property_style'], unique=False)
    op.create_index('ix_PropertyOriginal_apn', 'property_original', ['apn'], unique=False)
    op.create_index('ix_PropertyOriginal_block', 'property_original', ['block'], unique=False)
    op.create_index('ix_PropertyOriginal_county', 'property_original', ['county'], unique=False)
    op.create_index('ix_PropertyOriginal_lot', 'property_original', ['lot'], unique=False)
    op.create_index('ix_PropertyOriginal_number', 'property_original', ['number'], unique=False)
    op.create_index('ix_PropertyOriginal_print_key', 'property_original', ['print_key'], unique=False)
    op.create_index('ix_PropertyOriginal_school_district', 'property_original', ['school_district'], unique=False)
    op.create_index('ix_PropertyOriginal_section', 'property_original', ['section'], unique=False)
    op.create_index('ix_PropertyOriginal_state', 'property_original', ['state'], unique=False)
    op.create_index('ix_PropertyOriginal_street', 'property_original', ['street'], unique=False)
    op.create_index('ix_PropertyOriginal_town', 'property_original', ['town'], unique=False)
    op.create_index('ix_PropertyOriginal_undefined_field', 'property_original', ['undefined_field'], unique=False)
    op.create_index('ix_PropertyOriginal_village', 'property_original', ['village'], unique=False)
    op.create_index('ix_PropertyOriginal_zip', 'property_original', ['zip'], unique=False)
    op.create_unique_constraint('uc_PropertyOriginal_apn_county', 'property_original', ['apn', 'county'])
    op.drop_index('ix_property_address', table_name='property_original')
    op.drop_index('ix_property_apn', table_name='property_original')
    op.drop_index('ix_property_block', table_name='property_original')
    op.drop_index('ix_property_county', table_name='property_original')
    op.drop_index('ix_property_lot', table_name='property_original')
    op.drop_index('ix_property_number', table_name='property_original')
    op.drop_index('ix_property_print_key', table_name='property_original')
    op.drop_index('ix_property_school_district', table_name='property_original')
    op.drop_index('ix_property_section', table_name='property_original')
    op.drop_index('ix_property_state', table_name='property_original')
    op.drop_index('ix_property_street', table_name='property_original')
    op.drop_index('ix_property_town', table_name='property_original')
    op.drop_index('ix_property_undefined_field', table_name='property_original')
    op.drop_index('ix_property_village', table_name='property_original')
    op.drop_index('ix_property_zip', table_name='property_original')
    op.drop_index('property_another_combined_index', table_name='property_original')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('property_another_combined_index', 'property_original', ['county', 'school_district', 'property_class', 'town', 'street', 'property_style'], unique=False)
    op.create_index('ix_property_zip', 'property_original', ['zip'], unique=False)
    op.create_index('ix_property_village', 'property_original', ['village'], unique=False)
    op.create_index('ix_property_undefined_field', 'property_original', ['undefined_field'], unique=False)
    op.create_index('ix_property_town', 'property_original', ['town'], unique=False)
    op.create_index('ix_property_street', 'property_original', ['street'], unique=False)
    op.create_index('ix_property_state', 'property_original', ['state'], unique=False)
    op.create_index('ix_property_section', 'property_original', ['section'], unique=False)
    op.create_index('ix_property_school_district', 'property_original', ['school_district'], unique=False)
    op.create_index('ix_property_print_key', 'property_original', ['print_key'], unique=False)
    op.create_index('ix_property_number', 'property_original', ['number'], unique=False)
    op.create_index('ix_property_lot', 'property_original', ['lot'], unique=False)
    op.create_index('ix_property_county', 'property_original', ['county'], unique=False)
    op.create_index('ix_property_block', 'property_original', ['block'], unique=False)
    op.create_index('ix_property_apn', 'property_original', ['apn'], unique=False)
    op.create_index('ix_property_address', 'property_original', ['address'], unique=False)
    op.drop_constraint('uc_PropertyOriginal_apn_county', 'property_original', type_='unique')
    op.drop_index('ix_PropertyOriginal_zip', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_village', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_undefined_field', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_town', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_street', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_state', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_section', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_school_district', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_print_key', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_number', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_lot', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_county', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_block', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_apn', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_another_combined_index', table_name='property_original')
    op.drop_index('ix_PropertyOriginal_address', table_name='property_original')
    op.create_unique_constraint('_apn_county_uc', 'property', ['apn', 'county'])
    op.drop_constraint('uc_Property_apn_county', 'property', type_='unique')
    op.drop_index('ix_Property_zip', table_name='property')
    op.drop_index('ix_Property_village', table_name='property')
    op.drop_index('ix_Property_undefined_field', table_name='property')
    op.drop_index('ix_Property_town', table_name='property')
    op.drop_index('ix_Property_street', table_name='property')
    op.drop_index('ix_Property_state', table_name='property')
    op.drop_index('ix_Property_section', table_name='property')
    op.drop_index('ix_Property_school_district', table_name='property')
    op.drop_index('ix_Property_print_key', table_name='property')
    op.drop_index('ix_Property_number', table_name='property')
    op.drop_index('ix_Property_lot', table_name='property')
    op.drop_index('ix_Property_county', table_name='property')
    op.drop_index('ix_Property_block', table_name='property')
    op.drop_index('ix_Property_apn', table_name='property')
    op.drop_index('ix_Property_another_combined_index', table_name='property')
    op.drop_index('ix_Property_address', table_name='property')
    # ### end Alembic commands ###
