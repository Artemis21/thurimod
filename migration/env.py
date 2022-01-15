"""Alembic migration configuration."""
import asyncio
import shlex
import subprocess

from alembic import context
from alembic.script import write_hooks
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

import thurimod  # noqa: F401 - Import to register models.
from thurimod.database import DATABASE_URL, OrmBase

context.config.set_main_option("sqlalchemy.url", DATABASE_URL)


@write_hooks.register("poetry")
def poetry_autogen_hook(filename: str, options: dict[str, str]):
    """Run a Poetry command on an auto-generated migration."""
    if not (command := options.get("command")):
        name = options["_hook_name"]
        raise ValueError(f"Alembic post write hook {name!r} missing 'command' option.")
    args = shlex.split(command.format(filename=filename))
    subprocess.run(["poetry", "run", *args])


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an
    Engine is acceptable here as well. By skipping the Engine creation we don't
    even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.
    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=OrmBase.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    """Run all necessary connections."""
    context.configure(connection=connection, target_metadata=OrmBase.metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection
    with the context.
    """
    connectable = AsyncEngine(
        engine_from_config(
            context.config.get_section(context.config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)  # type: ignore


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
