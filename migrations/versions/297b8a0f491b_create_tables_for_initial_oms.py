"""Create tables for initial OMS

Revision ID: 297b8a0f491b
Revises: 1a59dda5b59b
Create Date: 2024-04-04 09:13:21.555064

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "297b8a0f491b"
down_revision: Union[str, None] = "1a59dda5b59b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "order_addresses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("street", sa.String(), nullable=False),
        sa.Column("number", sa.String(), nullable=False),
        sa.Column("neighborhood", sa.String(), nullable=False),
        sa.Column("complement", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("cep", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("order_address_id", sa.Integer(), nullable=False),
        sa.Column("total", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_address_id"],
            ["order_addresses.id"],
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.alter_column(
        "addresses", "complement", existing_type=sa.VARCHAR(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "addresses", "complement", existing_type=sa.VARCHAR(), nullable=False
    )
    op.drop_table("orders")
    op.drop_table("order_addresses")
    # ### end Alembic commands ###
