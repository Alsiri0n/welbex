from typing import Generic, TypeVar, Type, List
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from app.db.base_class import Base
from app.db.session import Session
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload
from sqlalchemy import select



ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        async with db.session() as session:
            q = select(ModelType). \
                options(subqueryload(ModelType.tracks))
            result: Result = await session.execute(q)
            user_model_full: UserModel = result.scalar()
            if user_model_full:
                q = select(TrackModel). \
                    where(and_(TrackModel.user_id == user_id, TrackModel.track_id == track_id))
                result: Result = await session.execute(q)
                track_model: UserModel = result.scalar()
                if track_model:
                    full_result = True
            else:
                return full_result
        return full_result

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh()
        return db_obj