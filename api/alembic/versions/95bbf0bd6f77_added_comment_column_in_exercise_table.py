"""added comment column in exercise table

Revision ID: 95bbf0bd6f77
Revises: 40be825ba2b4
Create Date: 2025-06-11 17:00:56.944792

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95bbf0bd6f77'
down_revision: Union[str, None] = '40be825ba2b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('exercise') as alter_table_user_op:
        alter_table_user_op.add_column(
            sa.Column("comment", sa.String(255), nullable=True)
                )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('exercise') as alter_table_user_op:
        alter_table_user_op.drop_column('comment')

