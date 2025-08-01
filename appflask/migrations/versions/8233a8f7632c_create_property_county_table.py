"""create property_county table

Revision ID: 8233a8f7632c
Revises: 8d40a3689d7a
Create Date: 2020-08-02 23:04:02.593120

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8233a8f7632c'
down_revision = '8d40a3689d7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('property_county',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('number', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.execute(
        '''
        INSERT INTO property_county (id, name, number) VALUES ('nassau', 'Nassau', null);
        INSERT INTO property_county (id, name, number) VALUES ('suffolk', 'Suffolk', null);
        INSERT INTO property_county (id, name, number) VALUES ('broward', 'Broward', 16);
        INSERT INTO property_county (id, name, number) VALUES ('miamidade', 'Miami Dade', 23);
        INSERT INTO property_county (id, name, number) VALUES ('palmbeach', 'Palm Beach', 60);
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('property_county')
    # ### end Alembic commands ###
