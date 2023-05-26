from random import randint
from sqlalchemy import func, select, update, Result, and_
from sqlalchemy.orm import subqueryload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.truck import TruckModel
from app.models.location import LocationModel
from app.schemas.truck import TruckBase


class CRUDTruck:
    async def create(self, db: AsyncSession):
        pass

    async def get(self, db: AsyncSession, id_: int) -> TruckModel:
        q = select(TruckModel) \
            .where(TruckModel.id == id_) \
            .options(subqueryload(TruckModel.location))
        result: Result = await db.execute(q)
        return result.scalar()

    async def update(self, db: AsyncSession, id_: int, location: int) -> TruckModel:
        q = update(TruckModel).where(TruckModel.id == id_).values(location_id=location)
        await db.execute(q)
        await db.commit()
        return await self.get(db, id_)

    async def remove(self, db: AsyncSession):
        pass

    async def create_init(self, db: AsyncSession, qnt: list) -> None:
        total: int = await db.scalar(select(func.count()).select_from(TruckModel))
        if not total:
            trucks: list = []
            for id_ in qnt:
                trucks.append(TruckModel(
                    number=str(randint(1000, 9999)) + chr(randint(65, 90)),
                    capacity=randint(1,1000),
                    location_id=id_,
                ))
            db.add_all(trucks)
            await db.commit()


truck = CRUDTruck()
