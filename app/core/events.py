from sqlalchemy.ext.asyncio import AsyncSession
from app.db.init_db import init_db
from app.db.session import engine


def create_start_app_handler(db: AsyncSession) -> None:
    async def start_app() -> None:
        await init_db(db)
    return start_app


def create_stop_app_handler(db: AsyncSession) -> None:
    async def stop_app() -> None:
        await db.close()
        await engine.dispose()
    return stop_app
