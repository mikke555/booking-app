"""add admin role

Revision ID: 23ef06704739
Revises: c395780dd363
Create Date: 2026-08-02 17:19:57.970657

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "23ef06704739"
down_revision: Union[str, Sequence[str], None] = "c395780dd363"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("is_admin", sa.Boolean(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "is_admin")
