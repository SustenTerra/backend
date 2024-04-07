"""fix address migration

Revision ID: a7332cc0a72f
Revises: aa7524b7039a
Create Date: 2024-04-04 09:02:57.178452

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a7332cc0a72f"
down_revision: Union[str, None] = "aa7524b7039a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("addresses", "created_at", nullable=True)
    op.execute("UPDATE addresses SET created_at = NOW() WHERE created_at IS NULL")
    op.alter_column("addresses", "created_at", nullable=False)

    op.alter_column("addresses", "updated_at", nullable=True)
    op.execute("UPDATE addresses SET updated_at = NOW() WHERE updated_at IS NULL")
    op.alter_column("addresses", "updated_at", nullable=False)


def downgrade() -> None:
    pass
