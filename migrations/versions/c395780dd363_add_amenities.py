"""add amenities

Revision ID: c395780dd363
Revises: 58a282b6c07d
Create Date: 2026-08-02 12:19:26.283464

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c395780dd363"
down_revision: Union[str, Sequence[str], None] = "58a282b6c07d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "amenities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "room_amenities",
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("amenity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["amenity_id"], ["amenities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("room_id", "amenity_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("room_amenities")
    op.drop_table("amenities")
