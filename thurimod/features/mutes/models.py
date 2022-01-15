"""Models related to the muting system."""
from sqlalchemy import BigInteger, Column

from ...database import OrmBase


class MuteSettings(OrmBase):
    """Global guild settings related to muting."""

    __tablename__ = "mute_settings"

    guild_id = Column(BigInteger, primary_key=True, autoincrement=False)
    mute_role = Column(BigInteger)
