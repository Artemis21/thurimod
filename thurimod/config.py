"""Load the Thurimod config options."""
import logging

import pydantic

from .utils.config_parse import BASE_PATH, LoggingOptions, parse_config

__all__ = ("CONFIG", "BASE_PATH")


class DiscordConfig(pydantic.BaseModel):
    """Discord related configuration options."""

    token: str
    guild_id: int
    admin_role_id: int


class DatabaseConfig(pydantic.BaseModel):
    """Database configuration options."""

    name: str = "thurimod"
    user: str = "thurimod"
    password: str
    host: str = "localhost"
    port: int = 5432


class LoggingConfig(pydantic.BaseModel):
    """Logging configuration options."""

    thurimod: LoggingOptions = LoggingOptions(level=logging.INFO)
    discord: LoggingOptions = LoggingOptions()
    interactions: LoggingOptions = LoggingOptions()
    sql: LoggingOptions = LoggingOptions()
    db: LoggingOptions = LoggingOptions()
    orm: LoggingOptions = LoggingOptions()
    postgres: LoggingOptions = LoggingOptions()
    migrations: LoggingOptions = LoggingOptions()


class EuterpeConfig(pydantic.BaseModel):
    """Configuration options for Euterpe."""

    discord: DiscordConfig
    database: DatabaseConfig
    logs: LoggingConfig = LoggingConfig()


CONFIG = parse_config("thurimod", EuterpeConfig)

CONFIG.logs.thurimod.apply("thurimod")
CONFIG.logs.discord.apply("nextcord")
CONFIG.logs.interactions.apply("discord_slash")
CONFIG.logs.sql.apply("sqlalchemy.engine")
CONFIG.logs.db.apply("sqlalchemy.pool")
CONFIG.logs.orm.apply("sqlalchemy.orm")
CONFIG.logs.postgres.apply("sqlalchemy.dialects")
CONFIG.logs.migrations.apply("alembic")
