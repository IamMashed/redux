"""update affected_age for broward and miamidade counties

Revision ID: 030a49ec57ad
Revises: 514eff96d359
Create Date: 2020-10-27 20:36:06.679181

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '030a49ec57ad'
down_revision = '514eff96d359'
branch_labels = None
depends_on = None


def upgrade():
    # op.execute(
    #     '''
    #     UPDATE property
    #     SET effective_age = bldg_year_built
    #     FROM helper.bcpa_tax_roll_ib_july_2020_final
    #     WHERE county = 'broward'
    #       AND apn = folio_number;
    #     '''
    # )
    #
    # op.execute(
    #     '''
    #
    #     UPDATE property
    #     SET effective_age = "EffectiveYearBuilt"
    #     FROM helper.miamidade_property_2020
    #     WHERE county = 'miamidade'
    #       AND apn = "Folio";
    #
    #     '''
    # )
    pass

def downgrade():
    pass
