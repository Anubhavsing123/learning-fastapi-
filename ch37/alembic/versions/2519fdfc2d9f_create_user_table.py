"""create user Table

Revision ID: 2519fdfc2d9f
Revises: 
Create Date: 2026-05-20 07:39:42.021413

"""
from typing import Sequence, Union


from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2519fdfc2d9f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# means creating table
def upgrade() -> None:
  op.create_table(
    "user",
    sa.Column("id", sa.INTEGER, primary_key=True),
    sa.Column("name", sa.String(50), nullable=False),
    sa.Column("email", sa.String(200))
   )

    

#down grade means delete of table
def downgrade() -> None:
   op.drop_table("user")
    
