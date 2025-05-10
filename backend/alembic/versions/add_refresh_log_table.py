"""create refresh_log table

Revision ID: add_refresh_log_table
Revises: 
Create Date: 2025-05-10 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_refresh_log_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'refresh_log',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('symbol', sa.String(), nullable=False),
        sa.Column('refreshed_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('status', sa.String(), nullable=True),
    )


def downgrade():
    op.drop_table('refresh_log')
