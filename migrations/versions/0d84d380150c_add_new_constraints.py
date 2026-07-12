"""add new constraints

Revision ID: 0d84d380150c
Revises: f2f919113dc6
Create Date: 2026-07-12 15:38:45.796800

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0d84d380150c"
down_revision: Union[str, Sequence[str], None] = "f2f919113dc6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint("hotels_name_key", "hotels", ["name"])
    op.create_check_constraint(
        "ck_rooms_quantity_positive",
        "rooms",
        sa.text("quantity >= 1"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("ck_rooms_quantity_positive", "rooms", type_="check")
    op.drop_constraint("hotels_name_key", "hotels", type_="unique")
