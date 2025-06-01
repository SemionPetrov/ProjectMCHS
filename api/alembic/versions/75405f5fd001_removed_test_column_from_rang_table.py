"""removed test column from rang table

Revision ID: 75405f5fd001
Revises: a5b45da38d44
Create Date: 2025-06-01 23:30:01.400107

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75405f5fd001'
down_revision: Union[str, None] = 'a5b45da38d44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
