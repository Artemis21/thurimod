"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision or "None" | comma,n}
Create Date: ${create_date}
"""
from alembic import op
import sqlalchemy as sa
${imports}

revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    """Apply the schema migration."""
    ${upgrades if upgrades else "pass"}


def downgrade():
    """Undo the schema migration."""
    ${downgrades if downgrades else "pass"}
