"""move assessment files into separate assessment_files table

Revision ID: 9b6077fb76a2
Revises: a418ffbe5937
Create Date: 2020-03-18 04:05:03.824501

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm

# revision identifiers, used by Alembic.
from app.settings.models import AssessmentDate, AssessmentFile

revision = '9b6077fb76a2'
down_revision = 'a418ffbe5937'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assessment_files',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('assessment_date_id', sa.Integer(), nullable=False),
                    sa.Column('file_name', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['assessment_date_id'], ['assessment_dates.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    assessment_dates = {
        1: 'TX451TWN5RS18400.TXT, TX451TWN1RS6400.TXT, TX451TWN1RS18400.TXT, TX451TWN1RS5400.TXT, TX451TWN2RS5400.TXT, '
           'TX451TWN2RS6400.TXT, TX451TWN2RS18400.TXT, TX451TWN3RS5400.TXT, TX451TWN3RS6400.TXT, TX451TWN3RS18400.TXT, '
           'TX451TWN3RS18405.TXT, TX451TWN4RS5400.TXT, TX451TWN4RS6400.TXT, TX451TWN4RS18400.TXT, TX451TWN5RS5400.TXT',
        2: 'assessment.txt',
        3: 'NAP60F201901.csv, NAL60F201902.csv',
        4: 'NAP23F201901.csv, NAL23F201901.csv',
        5: 'NAP16F201901.csv, NAL16F201901.csv',
        6: 'TX451TWN5RS18400.TXT, TX451TWN1RS6400.TXT, TX451TWN1RS18400.TXT, TX451TWN1RS5400.TXT, TX451TWN2RS5400.TXT, '
           'TX451TWN2RS6400.TXT, TX451TWN2RS18400.TXT, TX451TWN3RS5400.TXT, TX451TWN3RS6400.TXT, TX451TWN3RS18400.TXT, '
           'TX451TWN3RS18405.TXT, TX451TWN4RS5400.TXT, TX451TWN4RS6400.TXT, TX451TWN4RS18400.TXT, TX451TWN5RS5400.TXT',
        7: 'TX451TWN5RS18400.TXT, TX451TWN1RS6400.TXT, TX451TWN1RS18400.TXT, TX451TWN1RS5400.TXT, TX451TWN2RS5400.TXT, '
           'TX451TWN2RS6400.TXT, TX451TWN2RS18400.TXT, TX451TWN3RS5400.TXT, TX451TWN3RS6400.TXT, TX451TWN3RS18400.TXT, '
           'TX451TWN3RS18405.TXT, TX451TWN4RS5400.TXT, TX451TWN4RS6400.TXT, TX451TWN4RS18400.TXT, TX451TWN5RS5400.TXT'
    }

    # copy assessment file names to 'assessment_files' table
    for key in assessment_dates.keys():
        assessment_files = [x.strip() for x in assessment_dates[key].strip().split(',')]
        # print(assessment_files)

        for file in assessment_files:
            session.add(AssessmentFile(assessment_date_id=key, file_name=file))
        session.commit()

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assessment_files')
    # ### end Alembic commands ###
