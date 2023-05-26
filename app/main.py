from fastapi import FastAPI
from app.crud.views import api
from app.core.config import get_settings

from app.core.events import create_start_app_handler, create_stop_app_handler

from app.db.session import Session

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Main class for run application

def init_app():

    cur_app = FastAPI()
    db = Session()

    cur_app.add_event_handler(
        "startup",
        create_start_app_handler(db),
    )
    cur_app.add_event_handler(
        "shutdown",
        create_stop_app_handler(db),
    )

    cur_app.include_router(api)

    return cur_app


Application = init_app()
