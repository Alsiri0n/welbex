from typing import Generator

from app.db.session import Session

# Дополнительная функция для получения сессии
async def get_db() -> Generator:
    try:
        db = Session()
        yield db
    finally:
        await db.close()
