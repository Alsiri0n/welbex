from sqlalchemy import URL

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker
from app.core.config import get_settings

config = get_settings()

database_url = URL.create(
    drivername="postgresql+asyncpg",
    username=config.database_user,
    password=config.database_password,
    host=config.database_host,
    port=config.database_port,
    database=config.database_name,
)


engine: AsyncEngine = create_async_engine(database_url, echo=True)
Session: async_sessionmaker[AsyncSession] = async_sessionmaker(engine, expire_on_commit=False, autocommit=False,
                                                               autoflush=False)
