from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, Column, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.location import LocationModel


class TruckModel(Base):
    __tablename__ = "trucks"

    id = Column(BigInteger, primary_key=True)
    number = Column(Text, unique=True)
    capacity = Column(Integer)

    location_id = Column(BigInteger, ForeignKey("locations.id"))
    location = relationship("LocationModel", back_populates="trucks_location")
