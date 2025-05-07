"""expand stock_cache fields

Revision ID: 815ce5f23695
Revises: 42ca125e9338
Create Date: 2025-05-07 08:07:32.522912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '815ce5f23695'
down_revision: Union[str, None] = '42ca125e9338'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('stock_cache', sa.Column('name', sa.String(), nullable=True))
    op.add_column('stock_cache', sa.Column('exchange', sa.String(), nullable=True))
    op.add_column('stock_cache', sa.Column('change', sa.Float(), nullable=True))
    op.add_column('stock_cache', sa.Column('percent_change', sa.Float(), nullable=True))
    op.add_column('stock_cache', sa.Column('history', sa.String(), nullable=True))
    op.drop_column('stock_cache', 'change_percent')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('stock_cache', sa.Column('change_percent', sa.DOUBLE_PRECISION(precision=53), nullable=True))
    op.drop_column('stock_cache', 'history')
    op.drop_column('stock_cache', 'percent_change')
    op.drop_column('stock_cache', 'change')
    op.drop_column('stock_cache', 'exchange')
    op.drop_column('stock_cache', 'name')
