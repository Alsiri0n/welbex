from fastapi import APIRouter

from app.api.api_v1.endpoints import truck, cargo

api_router = APIRouter()

api_router.include_router(truck.router, prefix="/trucks", tags=["trucks"])
api_router.include_router(cargo.router, prefix="/cargos", tags=["cargos"])
