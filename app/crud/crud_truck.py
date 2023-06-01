from random import randint
from geopy.distance import geodesic as gd
from sqlalchemy import func, select, update, Result
from sqlalchemy.orm import subqueryload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.truck import TruckModel
from app.schemas.truck import TruckForInformation


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

    async def get_all_trucks(self, db: AsyncSession) -> list[TruckModel]:
        q = select(TruckModel).options(subqueryload(TruckModel.location))
        result: Result = await db.execute(q)

        total: list[TruckModel] = [r for r in result.scalars()]
        return total

    async def get_qnt_truck_by_distance(self, db: AsyncSession, lat: float, lng: float, miles: int = 1000) -> int:
        qnt = 0
        pickup_coord = (lat, lng)
        all_trucks = await self.get_all_trucks(db)
        for cur_truck in all_trucks:
            truck_coord = (cur_truck.location.lat, cur_truck.location.lng)
            if gd(pickup_coord, truck_coord).miles <= miles:
                qnt += 1
        return qnt

    async def get_truck_by_distance(self, db: AsyncSession, lat: float, lng: float, distance: int = -1) -> list[TruckForInformation]:
        cargo_coord = (lat, lng)
        all_trucks = await self.get_all_trucks(db)
        data: list[TruckForInformation] = []
        for cur_truck in all_trucks:
            cur_truck_coord = (cur_truck.location.lat, cur_truck.location.lng)
            cur_distance = int(gd(cargo_coord, cur_truck_coord).miles)
            if distance > 0 and cur_distance <= distance:
                data.append(TruckForInformation(number=cur_truck.number, distance=cur_distance))
            elif distance == -1:
                data.append(TruckForInformation(number=cur_truck.number, distance=cur_distance))
        return data


truck = CRUDTruck()
