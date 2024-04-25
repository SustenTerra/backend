"""add posts available quantity

Revision ID: c71808eede32
Revises: 297b8a0f491b
Create Date: 2024-04-07 10:59:29.817702

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c71808eede32"
down_revision: Union[str, None] = "297b8a0f491b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("posts", sa.Column("available_quantity", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("posts", "available_quantity")
    # ### end Alembic commands ###
