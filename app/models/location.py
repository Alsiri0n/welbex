from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, Column, Text, Float, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.cargo import CargoModel
    from app.models.truck import TruckModel


class LocationModel(Base):
    __tablename__ = "locations"

    id = Column(BigInteger, primary_key=True)
    town = Column(Text, nullable=False)
    state = Column(Text, nullable=False)
    zip = Column(Integer, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

    cargos_pickup = relationship("CargoModel", back_populates="pickup", foreign_keys="[CargoModel.pickup_id]")
    cargos_delivery = relationship("CargoModel", back_populates="delivery", foreign_keys="[CargoModel.delivery_id]")
    trucks_location = relationship("TruckModel", back_populates="location")
