from random import shuffle
from sqlalchemy import select, Result, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import LocationModel
from app.schemas.location import LocationSchema


class CRUDLocation:
    async def create(self, db: AsyncSession, obj_in: LocationSchema) -> LocationModel:
        db_obj = LocationModel(town=obj_in.town, state=obj_in.state, zip=obj_in.zip, lat=obj_in.lat, lng=obj_in.lng)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, postcode: int) -> LocationModel:
        q = select(LocationModel).where(LocationModel.zip == postcode)
        result: Result = await db.execute(q)
        l_m: LocationModel = result.scalar()
        return l_m

    async def update(self, db: AsyncSession):
        pass

    async def remove(self, db: AsyncSession):
        pass

    async def create_init(self, db: AsyncSession, obj_in: list[LocationSchema]) -> None:
        db_obj: list[LocationModel] = []
        for obj in obj_in:
            db_obj.append(LocationModel(town=obj.town, state=obj.state, zip=obj.zip, lat=obj.lat, lng=obj.lng))
        db.add_all(db_obj)
        await db.commit()

    async def get_first(self, db: AsyncSession) -> LocationModel | None:
        q = select(LocationModel).where(LocationModel.id == 1)
        result: Result = await db.execute(q)
        l_m: LocationModel = result.scalar_one_or_none()
        return l_m

    async def get_random_locations_id(self, db: AsyncSession, qnt: int) -> list[int]:
        total: int = await db.scalar(select(func.count()).select_from(LocationModel))
        lst = list(range(1, total + 1))
        shuffle(lst)
        return lst[:qnt]


location = CRUDLocation()