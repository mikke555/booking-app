"""add cancelled_at attr to booking model

Revision ID: 1b39527be874
Revises: 980279586032
Create Date: 2026-08-04 11:08:22.411362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b39527be874'
down_revision: Union[str, Sequence[str], None] = '980279586032'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('bookings', sa.Column('cancelled_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('bookings', 'cancelled_at')
