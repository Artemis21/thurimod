"""Sets up the database connection."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import declarative_base

from .config import CONFIG

DATABASE_URL = "postgresql+asyncpg://{0.user}:{0.password}@{0.host}:{0.port}/{0.name}".format(
    CONFIG.database
)
engine = create_async_engine(DATABASE_URL, future=True)
OrmBase = declarative_base()
make_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
