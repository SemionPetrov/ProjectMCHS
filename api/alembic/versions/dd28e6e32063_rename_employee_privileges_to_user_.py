"""Rename employee_privileges to user_privilege

Revision ID: dd28e6e32063
Revises: 0352cf6ef74c
Create Date: 2025-06-03 17:00:31.021237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd28e6e32063'
down_revision: Union[str, None] = '0352cf6ef74c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table('employee_privileges', 'user_privilege')


def downgrade() -> None:
    """Downgrade schema."""
    op.rename_table('user_privilege', 'employee_privileges')
