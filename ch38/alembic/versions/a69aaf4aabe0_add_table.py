"""add table

Revision ID: a69aaf4aabe0
Revises: 
Create Date: 2026-05-20 23:17:11.638087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a69aaf4aabe0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.create_table(
    "user",
    sa.Column("id", sa.INTEGER, primary_key=True),
    sa.Column("name", sa.String(50), nullable=False),
    sa.Column("email", sa.String(20))
   )


def downgrade() -> None:
    op.drop_table("user")