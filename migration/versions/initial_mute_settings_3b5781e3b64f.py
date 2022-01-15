"""Initial mute settings.

Revision ID: 3b5781e3b64f
Revises: 9a65d456bc11
Create Date: 2021-10-29 03:28:19.043329
"""
import sqlalchemy as sa
from alembic import op

revision = "3b5781e3b64f"
down_revision = "9a65d456bc11"
branch_labels = None
depends_on = None


def upgrade():
    """Apply the schema migration."""
    op.create_table(
        "mute_settings",
        sa.Column("guild_id", sa.BigInteger(), autoincrement=False, nullable=False),
        sa.Column("mute_role", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("guild_id"),
    )


def downgrade():
    """Undo the schema migration."""
    op.drop_table("mute_settings")
