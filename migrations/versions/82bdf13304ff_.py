"""empty message

Revision ID: 82bdf13304ff
Revises: 
Create Date: 2017-09-07 00:01:26.586000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82bdf13304ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('betfreds', sa.Column('dateto', sa.Date(), nullable=True))
    op.create_unique_constraint(None, 'betfreds', ['dateto'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'betfreds', type_='unique')
    op.drop_column('betfreds', 'dateto')
    # ### end Alembic commands ###