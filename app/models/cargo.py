from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, Column, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.schemas.cargo import CargoSchema

if TYPE_CHECKING:
    from .location import LocationModel


class CargoModel(Base):
    __tablename__ = "cargos"
    id = Column(BigInteger, primary_key=True)
    weight = Column(Integer, nullable=False)
    description = Column(Text)

    pickup_id = Column(BigInteger, ForeignKey("locations.id"))
    delivery_id = Column(BigInteger, ForeignKey("locations.id"))

    pickup = relationship("LocationModel", back_populates="cargos_pickup", foreign_keys="[CargoModel.pickup_id]")
    delivery = relationship("LocationModel", back_populates="cargos_delivery", foreign_keys="[CargoModel.delivery_id]")

