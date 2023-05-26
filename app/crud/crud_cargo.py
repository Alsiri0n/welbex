from sqlalchemy import select, delete, Result, update
from sqlalchemy.orm import subqueryload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cargo import CargoModel
from app.schemas.cargo import CargoSchema


class CRUDCargo:
    async def create(self, db: AsyncSession, obj_in: CargoSchema) -> CargoModel:
        db_obj = CargoModel(
            weigh=obj_in.weight,
            description=obj_in.description,
            pickup_id=obj_in.pickup_id,
            deliver_id=obj_in.delivery_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, id_: int) -> CargoModel:
        q = select(CargoModel)\
            .where(CargoModel.id == id_)\
            .options(subqueryload(CargoModel.pickup))\
            .options(subqueryload(CargoModel.delivery))
        result: Result = await db.execute(q)
        return result.scalar()

    async def update(self, db: AsyncSession, id_: int, weight: int = -1, description: str = ""):
        q = update(CargoModel).\
            where(CargoModel.id == id_).\
            values(weight=weight, description=description)
        result: Result = await db.execute(q)
        await db.commit()
        return result.scalar()

    async def remove(self, db: AsyncSession, id_: int):
        q = delete(CargoModel).where(CargoModel.id == id_)
        result: Result = await db.execute(q)
        await db.commit()

    async def list_cargo(self, db: AsyncSession):
        pass


cargo = CRUDCargo()
