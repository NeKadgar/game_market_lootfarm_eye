"""dota item

Revision ID: bfebedc9b9c9
Revises: 
Create Date: 2022-06-17 13:21:53.480614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfebedc9b9c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dota_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('dota_item_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('max_count', sa.Integer(), nullable=True),
    sa.Column('site_rate', sa.Integer(), nullable=True),
    sa.Column('in_trade', sa.Integer(), nullable=True),
    sa.Column('in_reserve', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('dota_item_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dota_item_id'], ['dota_item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dota_item_history_dota_item_id'), 'dota_item_history', ['dota_item_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dota_item_history_dota_item_id'), table_name='dota_item_history')
    op.drop_table('dota_item_history')
    op.drop_table('dota_item')
    # ### end Alembic commands ###
