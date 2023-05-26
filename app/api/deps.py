from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
# from sqlalchemy.orm import Session


from app.db.session import Session


async def get_db() -> Generator:
    try:
        db = Session()
        yield db
    finally:
        await db.close()
