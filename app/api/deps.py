from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas

from app.core.config import get_settings
from app.db.session import Session


async def get_db() -> Generator:
    try:
        db = Session()
        yield db
    finally:
        await db.close()
