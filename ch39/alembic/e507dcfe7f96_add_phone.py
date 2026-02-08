"""add phone

Revision ID: e507dcfe7f96
Revises: a69aaf4aabe0
Create Date: 2026-05-20 23:20:46.694775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e507dcfe7f96'
down_revision: Union[str, Sequence[str], None] = 'a69aaf4aabe0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.add_column("user",sa.Column("phone",sa.Integer()))


def downgrade() -> None:
    op.drop_column("user","phone")
    
