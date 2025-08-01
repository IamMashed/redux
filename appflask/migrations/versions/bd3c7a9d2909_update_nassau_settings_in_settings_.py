"""update settings in settings_global table

Revision ID: bd3c7a9d2909
Revises: 35db97217128
Create Date: 2020-03-16 15:28:19.418679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd3c7a9d2909'
down_revision = '35db97217128'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        insert into settings_global (county, settings) 
        values ('nassau', '{"pdf_header": "PROPERTY TAX REDUCTION CONSULTANTS 125 JERICHO TPKE, SUITE 500, JERICHO NY 11753 516-474-0654 516-484-2565 (FAX)"}');
        
        insert into settings_global(county, settings)
        values ('suffolk', '{}');

        insert into settings_global(county, settings)
        values ('broward', '{}');

        insert into settings_global(county, settings)
        values ('miamidade', '{}');

        insert into settings_global(county, settings)
        values ('palmbeach', '{}');
        
        insert into settings_global(county, settings)
        values (NULL, '{}');

        '''
    )

    # op.execute(
    #     '''
    #     update settings_global
    #     set county = NULL
    #     '''
    # )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
        delete from settings_global;
        '''
    )
    # ### end Alembic commands ###
