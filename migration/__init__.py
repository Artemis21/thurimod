"""Alembic migrations."""
from alembic import command, config

from thurimod.config import BASE_PATH


def upgrade_db(revision: str = "head"):
    """Upgrade database to a given revision."""
    alembic_config = config.Config(f"{BASE_PATH}/alembic.ini")
    command.upgrade(alembic_config, revision)
