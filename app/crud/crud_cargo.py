from sqlalchemy import select, delete, Result, update
from sqlalchemy.orm import subqueryload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cargo import CargoModel
from app.schemas.cargo import CargoBase


class CRUDCargo:
    async def create(self, db: AsyncSession, obj_in: CargoBase) -> CargoModel:
        db_obj = CargoModel(
            weight=obj_in.weight,
            description=obj_in.description,
            pickup_id=obj_in.pickup_id,
            delivery_id=obj_in.delivery_id,
        )
        db.add(db_obj)
        await db.commit()

        return await self.get(db, db_obj.id)

    async def get(self, db: AsyncSession, id_: int) -> CargoModel:
        q = select(CargoModel)\
            .where(CargoModel.id == id_)\
            .options(subqueryload(CargoModel.pickup))\
            .options(subqueryload(CargoModel.delivery))
        result: Result = await db.execute(q)
        return result.scalar()

    async def update(self, db: AsyncSession, id_: int, weight: int, description: str) -> CargoModel:
        q = update(CargoModel).\
            where(CargoModel.id == id_).\
            values(weight=weight, description=description)
        await db.execute(q)
        await db.commit()
        return await self.get(db, id_)

    async def remove(self, db: AsyncSession, cargo_model: CargoModel) -> CargoModel:
        await db.delete(cargo_model)
        await db.commit()
        return cargo_model

    async def list_cargo(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> list[CargoModel]:
        cargos = []
        q = select(CargoModel)\
            .offset(skip)\
            .limit(limit)\
            .options(subqueryload(CargoModel.pickup))\
            .options(subqueryload(CargoModel.delivery))
        result: Result = await db.execute(q)
        if result:
            cargos = [r for r in result.scalars()]
        return cargos

cargo = CRUDCargo()
