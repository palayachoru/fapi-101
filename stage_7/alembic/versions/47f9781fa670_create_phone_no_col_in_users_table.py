"""create phone no col in users table

Revision ID: 47f9781fa670
Revises:
Create Date: 2026-09-03 01:10:23.960185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import models

# revision identifiers, used by Alembic.
revision: str = '47f9781fa670'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_no', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('usrs', 'phone_no')
