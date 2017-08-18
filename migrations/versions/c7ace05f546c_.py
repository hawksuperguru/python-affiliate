"""empty message

Revision ID: c7ace05f546c
Revises: d96a6485b675
Create Date: 2017-08-14 21:09:04.085264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7ace05f546c'
down_revision = 'd96a6485b675'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stans', sa.Column('clito', sa.Integer(), nullable=True))
    op.add_column('stans', sa.Column('cliytd', sa.Integer(), nullable=True))
    op.add_column('stans', sa.Column('commito', sa.Float(), nullable=True))
    op.add_column('stans', sa.Column('commiytd', sa.Float(), nullable=True))
    op.add_column('stans', sa.Column('imprto', sa.Integer(), nullable=True))
    op.add_column('stans', sa.Column('imprytd', sa.Integer(), nullable=True))
    op.add_column('stans', sa.Column('ndto', sa.Integer(), nullable=True))
    op.add_column('stans', sa.Column('ndytd', sa.Integer(), nullable=True))
    op.add_column('stans', sa.Column('regto', sa.Integer(), nullable=True))
    op.add_column('stans', sa.Column('regytd', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stans', 'regytd')
    op.drop_column('stans', 'regto')
    op.drop_column('stans', 'ndytd')
    op.drop_column('stans', 'ndto')
    op.drop_column('stans', 'imprytd')
    op.drop_column('stans', 'imprto')
    op.drop_column('stans', 'commiytd')
    op.drop_column('stans', 'commito')
    op.drop_column('stans', 'cliytd')
    op.drop_column('stans', 'clito')
    # ### end Alembic commands ###