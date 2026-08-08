"""unify price/qty constraints

Revision ID: 41a063baa595
Revises: 1b39527be874
Create Date: 2026-08-04 15:15:00.188941

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "41a063baa595"
down_revision: Union[str, Sequence[str], None] = "1b39527be874"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        "ck_rooms_quantity_positive",
        "rooms",
        type_="check",
    )
    op.create_check_constraint(
        "ck_rooms_quantity_positive",
        "rooms",
        sa.text("quantity > 0"),
    )
    op.create_check_constraint(
        "ck_rooms_price_positive",
        "rooms",
        sa.text("price > 0"),
    )

    op.drop_constraint(
        "ck_bookings_price_non_negative",
        "bookings",
        type_="check",
    )
    op.create_check_constraint(
        "ck_bookings_price_positive",
        "bookings",
        sa.text("price > 0"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "ck_bookings_price_positive",
        "bookings",
        type_="check",
    )
    op.create_check_constraint(
        "ck_bookings_price_non_negative",
        "bookings",
        sa.text("price >= 0"),
    )

    op.drop_constraint(
        "ck_rooms_price_positive",
        "rooms",
        type_="check",
    )
    op.drop_constraint(
        "ck_rooms_quantity_positive",
        "rooms",
        type_="check",
    )
    op.create_check_constraint(
        "ck_rooms_quantity_positive",
        "rooms",
        sa.text("quantity >= 1"),
    )
