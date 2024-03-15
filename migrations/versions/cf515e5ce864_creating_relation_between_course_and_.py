"""Creating relation between Course and User

Revision ID: cf515e5ce864
Revises: f5e46b64710f
Create Date: 2024-03-15 11:16:08.493291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cf515e5ce864"
down_revision: Union[str, None] = "f5e46b64710f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "courses", sa.Column("author_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        "author_courses_fkey", "courses", "users", ["author_id"], ["id"]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("author_courses_fkey", "courses", type_="foreignkey")
    op.drop_column("courses", "author_id")
    # ### end Alembic commands ###
