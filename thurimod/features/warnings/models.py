"""SQLAlchemy models for the warning system."""
from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from ...database import OrmBase


class Warning(OrmBase):
    """An SQLAlchemy model for a warning."""

    __tablename__ = "warning"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    reason = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
