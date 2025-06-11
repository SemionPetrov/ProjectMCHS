"""ondelete/onupdate for excercise-excercieReport

Revision ID: 40be825ba2b4
Revises: 65b7b1d7b541
Create Date: 2025-06-11 15:40:00.225000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40be825ba2b4'
down_revision: Union[str, None] = '65b7b1d7b541'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('user') as alter_table_user_op:
        alter_table_user_op.add_column(
            sa.Column("contact_info", sa.String(100), nullable=True, unique=True)
                )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('user') as alter_table_user_op:
        alter_table_user_op.drop_column('contact_info')
