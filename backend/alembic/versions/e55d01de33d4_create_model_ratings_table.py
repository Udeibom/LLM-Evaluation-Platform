"""create model_ratings table

Revision ID: e55d01de33d4
Revises: 23e10a010b7b
Create Date: 2026-03-16 11:59:17.919099
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e55d01de33d4"
down_revision: Union[str, Sequence[str], None] = "23e10a010b7b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "model_ratings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("model_name", sa.String(), nullable=False, unique=True),
        sa.Column("elo_rating", sa.Float(), nullable=False, server_default="1000"),
        sa.Column("matches_played", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("wins", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("losses", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("ties", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("model_ratings")