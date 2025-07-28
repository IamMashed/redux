"""suffolk district update

Revision ID: 6607f6fc39ca
Revises: 980aeb472420
Create Date: 2020-11-06 22:01:50.261081

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6607f6fc39ca'
down_revision = '980aeb472420'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        '''
        UPDATE property
        SET district = (CASE
                            WHEN substring(apn, 0, 3) = '01' THEN '100'
                            WHEN substring(apn, 0, 3) = '02' THEN '200'
                            WHEN substring(apn, 0, 3) = '03' THEN '300'
                            WHEN substring(apn, 0, 3) = '04' THEN '400'
                            WHEN substring(apn, 0, 3) = '05' THEN '500'
                            WHEN substring(apn, 0, 3) = '06' THEN '600'
                            WHEN substring(apn, 0, 3) = '07' THEN '700'
                            WHEN substring(apn, 0, 3) = '08' THEN '800'
                            WHEN substring(apn, 0, 3) = '09' THEN '900'
                            WHEN substring(apn, 0, 3) = '10' THEN '1000'
            END
            )
        WHERE county = 'suffolk';


        CREATE INDEX property_district_idx
            ON property (lower(district::text));
        '''
    )


def downgrade():
    pass
