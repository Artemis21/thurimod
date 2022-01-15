"""Create the initial table for the warnings system..

Revision ID: 9a65d456bc11
Revises: None
Create Date: 2021-10-28 23:55:10.822464
"""
import sqlalchemy as sa
from alembic import op

revision = "9a65d456bc11"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Apply the schema migration."""
    op.create_table(
        "warning",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("reason", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    """Undo the schema migration."""
    op.drop_table("warning")
