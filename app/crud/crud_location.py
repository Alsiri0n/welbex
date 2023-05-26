from typing import List
from app.db.session import Session
from app.models.location import LocationModel
from app.schemas.location import LocationSchema
from sqlalchemy import select, Result


class CRUDLocation:
    async def create(self, db: Session, obj_in: LocationSchema) -> LocationModel:
        db_obj = LocationModel(town=obj_in.town, state=obj_in.state, zip=obj_in.zip, lat=obj_in.lat, lng=obj_in.lng)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    def get(self, db: Session):
        pass

    def update(self, db: Session):
        pass

    def remove(self, db: Session):
        pass

    async def create_init(self, db: Session, obj_in: List[LocationSchema]) -> None:
        db_obj: List[LocationModel] = []
        for obj in obj_in:
            db_obj.append(LocationModel(town=obj.town, state=obj.state, zip=obj.zip, lat=obj.lat, lng=obj.lng))
        db.add_all(db_obj)
        await db.commit()

    async def get_first(self, db: Session) -> LocationModel | None:
        q = select(LocationModel).where(LocationModel.id == 1)
        result: Result = await db.execute(q)
        l_m: LocationModel = result.scalar_one_or_none()
        return l_m




location = CRUDLocation()