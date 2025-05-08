"""add watchlist table

Revision ID: 78331270068e
Revises: c4fa779ab085
Create Date: 2025-05-08 05:19:57.499579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78331270068e'
down_revision: Union[str, None] = 'c4fa779ab085'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'watchlist',
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('symbol', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.uid']),
        sa.ForeignKeyConstraint(['symbol'], ['stock_cache.symbol']),
        sa.PrimaryKeyConstraint('user_id', 'symbol')
    )

def downgrade():
    op.drop_table('watchlist')
