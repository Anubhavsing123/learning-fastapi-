"""add address

Revision ID: 66fcbccc9c83
Revises: e507dcfe7f96
Create Date: 2026-05-20 23:36:11.947665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66fcbccc9c83'
down_revision: Union[str, Sequence[str], None] = 'e507dcfe7f96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user", sa.Column("address", sa.String()))


def downgrade() -> None:
    op.drop_column("user", "address")
