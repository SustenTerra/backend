"""Change course image_url to image_key

Revision ID: 0cf73448e24c
Revises: 4aaf931930f7
Create Date: 2024-04-02 11:35:57.457362

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0cf73448e24c"
down_revision: Union[str, None] = "4aaf931930f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("courses", sa.Column("image_key", sa.String(), nullable=True))
    op.drop_column("courses", "image_url")

    op.execute(
        """
        UPDATE courses
        SET image_key = 'banner.png'
        """
    )
    op.alter_column("courses", "image_key", nullable=False)


def downgrade() -> None:
    op.add_column(
        "courses",
        sa.Column("image_url", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("courses", "image_key")

    op.execute(
        """
        UPDATE courses
        SET image_url = 'https://sustenterra.netlify.app/logo192.png'
        """
    )
    op.alter_column("courses", "image_url", nullable=False)
