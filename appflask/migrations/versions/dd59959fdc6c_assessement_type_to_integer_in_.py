"""assessement_type to integer in assessment_dates table

Revision ID: dd59959fdc6c
Revises: 3e47beb573c7
Create Date: 2020-02-07 17:50:14.797376

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'dd59959fdc6c'
down_revision = '3e47beb573c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('assessment_dates', 'assessment_month',
                    existing_type=sa.INTEGER(),
                    nullable=False)
    op.alter_column('assessment_dates', 'assessment_year',
                    existing_type=sa.INTEGER(),
                    nullable=False)

    op.execute(
        '''
            UPDATE assessment_dates 
            SET assessment_type=1 
            WHERE assessment_type='final';
        '''
    )

    op.execute(
        '''
            UPDATE assessment_dates 
            SET assessment_type=2 
            WHERE assessment_type='tentative';
        '''
    )

    op.execute(
        '''
            UPDATE assessment_dates 
            SET assessment_type=3 
            WHERE assessment_type='school';
        '''
    )

    op.alter_column('assessment_dates', 'assessment_type',
                    existing_type=sa.VARCHAR(length=255),
                    type_=sa.Integer(),
                    nullable=False,
                    postgresql_using='assessment_type::integer')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('assessment_dates', 'assessment_year',
                    existing_type=sa.INTEGER(),
                    nullable=True)
    op.alter_column('assessment_dates', 'assessment_type',
                    existing_type=sa.Integer(),
                    type_=sa.VARCHAR(length=255),
                    nullable=True)
    op.alter_column('assessment_dates', 'assessment_month',
                    existing_type=sa.INTEGER(),
                    nullable=True)
    # ### end Alembic commands ###
