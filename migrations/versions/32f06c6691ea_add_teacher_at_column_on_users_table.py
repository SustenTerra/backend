"""Add teacher_at column on users table

Revision ID: 32f06c6691ea
Revises: 4b12947b3404
Create Date: 2024-03-04 20:02:52.286021

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "32f06c6691ea"
down_revision: Union[str, None] = "4b12947b3404"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("teacher_at", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "teacher_at")
    # ### end Alembic commands ###
