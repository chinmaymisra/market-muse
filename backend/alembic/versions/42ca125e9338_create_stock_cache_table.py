"""create stock_cache table

Revision ID: 42ca125e9338
Revises: 
Create Date: 2025-05-07 07:41:15.139703

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42ca125e9338'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create only stock_cache table
    op.create_table(
        'stock_cache',
        sa.Column('symbol', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('change_percent', sa.Float(), nullable=True),
        sa.Column('volume', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('symbol')
    )
    op.create_index(op.f('ix_stock_cache_symbol'), 'stock_cache', ['symbol'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_stock_cache_symbol'), table_name='stock_cache')
    op.drop_table('stock_cache')
