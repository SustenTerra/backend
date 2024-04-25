"""add stripe product id

Revision ID: 1c7168d6b438
Revises: c71808eede32
Create Date: 2024-04-25 14:37:23.991311

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1c7168d6b438"
down_revision: Union[str, None] = "c71808eede32"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("posts", sa.Column("stripe_product_id", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("posts", "stripe_product_id")
    # ### end Alembic commands ###
