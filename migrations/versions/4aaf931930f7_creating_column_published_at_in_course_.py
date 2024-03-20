"""Creating column published_at in Course table

Revision ID: 4aaf931930f7
Revises: cf515e5ce864
Create Date: 2024-03-20 10:19:41.257299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4aaf931930f7"
down_revision: Union[str, None] = "cf515e5ce864"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "courses", sa.Column("published_at", sa.DateTime(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("courses", "published_at")
    # ### end Alembic commands ###
