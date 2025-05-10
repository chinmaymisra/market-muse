"""create settings table

Revision ID: add_settings_table
Revises: 
Create Date: 2025-05-10 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_settings_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'settings',
        sa.Column('key', sa.String(), primary_key=True, index=True),
        sa.Column('value', sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table('settings')
