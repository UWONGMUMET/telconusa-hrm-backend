"""Fix user account columns

Revision ID: c600084c58f6
Revises: 37184c6c4f5b
Create Date: 2026-11-25 22:55:34.738128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c600084c58f6'
down_revision: Union[str, Sequence[str], None] = '37184c6c4f5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "bool",
        new_column_name="is_active",
        existing_type=sa.Boolean(),
    )
    op.create_unique_constraint(
        "users_employee_id_key",
        "users",
        ["employee_id"],
    )


def downgrade() -> None:
    op.drop_constraint("users_employee_id_key", "users", type_="unique")
    op.alter_column(
        "users",
        "is_active",
        new_column_name="bool",
        existing_type=sa.Boolean(),
    )