"""Parses an INI file for config options."""
from __future__ import annotations

import logging
import pathlib
import sys
from typing import Any, Callable, Iterator, Type, TypeVar, Union

import pydantic
import toml
from rich.logging import RichHandler

BASE_PATH = pathlib.Path(__file__).parent.parent.parent
CONFIG_PATH = BASE_PATH / "config.toml"
RAW_CONFIG = toml.load(CONFIG_PATH)


class LogLevel(int):
    """Pydantic validator for a logging level."""

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable]:
        """Get the validator for a log level."""
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, int]) -> LogLevel:
        """Validate and convert a log level."""
        if isinstance(value, int):
            return LogLevel(value)
        try:
            return LogLevel(value)  # Convert to int.
        except ValueError:
            pass
        try:
            return LogLevel(
                {
                    "critical": logging.CRITICAL,
                    "error": logging.ERROR,
                    "warning": logging.WARNING,
                    "info": logging.INFO,
                    "debug": logging.DEBUG,
                    "notset": logging.NOTSET,
                    "none": logging.NOTSET,
                }[value.lower()]
            )
        except KeyError as e:
            raise ValueError(f'Invalid log level name "{value}".') from e

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]):
        """Update the schema to show this field."""
        field_schema.update(
            pattern="^([0-9]+|NONE|NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
            examples=[20, "INFO", "critical", 50, "none"],
        )


class LoggingOptions(pydantic.BaseModel):
    """Configuration options for some logging namespace."""

    level: LogLevel = LogLevel(logging.WARNING)

    def apply(self, namespace: str):
        """Apply this log level to a logging namespace."""
        logger = logging.getLogger(namespace)
        logger.addHandler(RichHandler(rich_tracebacks=True))
        logger.setLevel(level=self.level)


def config_error(message: str):
    """Print an error message and exit."""
    print("Error: " + message, file=sys.stderr)
    sys.exit(1)


T = TypeVar("T", bound=pydantic.BaseModel)


def parse_config(section: str, options: Type[T]) -> T:
    """Parse a section of the config file for specified options."""
    try:
        data = RAW_CONFIG[section]
    except KeyError:
        config_error(f"Section {section} not found in config.ini.")
    data = {key.replace("-", "_").lower(): value for key, value in data.items()}
    try:
        return options(**data)
    except pydantic.ValidationError as error:
        config_error(f"Error parsing {section} config:\n{error}")
