from fastapi import FastAPI

from sqlalchemy.ext.asyncio import AsyncSession
from app.api.api_v1.api import api_router

from app.core.events import create_start_app_handler, create_stop_app_handler

from app.db.session import Session

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Main class for run application
def init_app():

    cur_app = FastAPI()
    db: AsyncSession = Session()

    cur_app.add_event_handler(
        "startup",
        create_start_app_handler(db),
    )
    cur_app.add_event_handler(
        "shutdown",
        create_stop_app_handler(db),
    )

    cur_app.include_router(api_router)

    return cur_app


Application = init_app()
