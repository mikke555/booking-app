"""add composite index on bookings room and dates

Revision ID: 58a282b6c07d
Revises: 0d84d380150c
Create Date: 2026-08-01 16:29:00.243556

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "58a282b6c07d"
down_revision: Union[str, Sequence[str], None] = "0d84d380150c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
        "ix_bookings_room_dates",
        "bookings",
        ["room_id", "date_from", "date_to"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_bookings_room_dates", table_name="bookings")
