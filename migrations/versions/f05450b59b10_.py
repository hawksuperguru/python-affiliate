"""empty message

Revision ID: f05450b59b10
Revises: 2c5e1c4ab272
Create Date: 2017-09-08 11:10:22.489000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f05450b59b10'
down_revision = '2c5e1c4ab272'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ladbrokes', sa.Column('click', sa.Integer(), nullable=True))
    op.add_column('ladbrokes', sa.Column('clito', sa.Integer(), nullable=True))
    op.add_column('ladbrokes', sa.Column('cliytd', sa.Integer(), nullable=True))
    op.add_column('ladbrokes', sa.Column('commission', sa.Float(), nullable=True))
    op.add_column('ladbrokes', sa.Column('commito', sa.Float(), nullable=True))
    op.add_column('ladbrokes', sa.Column('commiytd', sa.Float(), nullable=True))
    op.add_column('ladbrokes', sa.Column('impression', sa.Integer(), nullable=True))
    op.add_column('ladbrokes', sa.Column('impreto', sa.Integer(), nullable=True))
    op.add_column('ladbrokes', sa.Column('impreytd', sa.Integer(), nullable=True))
    op.add_column('ladbrokes', sa.Column('merchant', sa.String(length=80), nullable=True))
    op.add_column('ladbrokes', sa.Column('ndto', sa.Integer(), nullable=True))
    op.add_column('ladbrokes', sa.Column('ndytd', sa.Integer(), nullable=True))
    op.add_column('ladbrokes', sa.Column('new_deposit', sa.Integer(), nullable=True))
    op.add_column('ladbrokes', sa.Column('registration', sa.Integer(), nullable=True))
    op.add_column('ladbrokes', sa.Column('regto', sa.Integer(), nullable=True))
    op.add_column('ladbrokes', sa.Column('regytd', sa.Integer(), nullable=True))
    op.drop_column('ladbrokes', 'CPA_COMMISSION')
    op.drop_column('ladbrokes', 'SPORTS_SIGNUPS')
    op.drop_column('ladbrokes', 'STAT_DATE')
    op.drop_column('ladbrokes', 'ACQUIRED_COUNT')
    op.drop_column('ladbrokes', 'SPORTS_NET_GAMING_REVENUE')
    op.drop_column('ladbrokes', 'NG_COMMISSION')
    op.drop_column('ladbrokes', 'REAL_IMPS')
    op.drop_column('ladbrokes', 'WITHDRAWS_CNT')
    op.drop_column('ladbrokes', 'RAW_CLICKS')
    op.drop_column('ladbrokes', 'RAW_IMPS')
    op.drop_column('ladbrokes', 'REAL_CLICKS')
    op.drop_column('ladbrokes', 'SPORTS_ACQUIRED_COUNT')
    op.drop_column('ladbrokes', 'TLR_AMOUNT')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ladbrokes', sa.Column('TLR_AMOUNT', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('ladbrokes', sa.Column('SPORTS_ACQUIRED_COUNT', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('ladbrokes', sa.Column('REAL_CLICKS', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('ladbrokes', sa.Column('RAW_IMPS', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('ladbrokes', sa.Column('RAW_CLICKS', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('ladbrokes', sa.Column('WITHDRAWS_CNT', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('ladbrokes', sa.Column('REAL_IMPS', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('ladbrokes', sa.Column('NG_COMMISSION', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('ladbrokes', sa.Column('SPORTS_NET_GAMING_REVENUE', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('ladbrokes', sa.Column('ACQUIRED_COUNT', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('ladbrokes', sa.Column('STAT_DATE', sa.DATE(), autoincrement=False, nullable=True))
    op.add_column('ladbrokes', sa.Column('SPORTS_SIGNUPS', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('ladbrokes', sa.Column('CPA_COMMISSION', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('ladbrokes', 'regytd')
    op.drop_column('ladbrokes', 'regto')
    op.drop_column('ladbrokes', 'registration')
    op.drop_column('ladbrokes', 'new_deposit')
    op.drop_column('ladbrokes', 'ndytd')
    op.drop_column('ladbrokes', 'ndto')
    op.drop_column('ladbrokes', 'merchant')
    op.drop_column('ladbrokes', 'impreytd')
    op.drop_column('ladbrokes', 'impreto')
    op.drop_column('ladbrokes', 'impression')
    op.drop_column('ladbrokes', 'commiytd')
    op.drop_column('ladbrokes', 'commito')
    op.drop_column('ladbrokes', 'commission')
    op.drop_column('ladbrokes', 'cliytd')
    op.drop_column('ladbrokes', 'clito')
    op.drop_column('ladbrokes', 'click')
    # ### end Alembic commands ###