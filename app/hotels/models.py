from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Hotel(Base):
    __tablename__ = 'hotels'
    # id: Mapped[int] = mapped_column(primary_key=True)
    # name: Mapped[str]
    # location: Mapped[str]
    # services: Mapped[str]
    # rooms_quantity: Mapped[int]
    # image_id: Mapped[int]

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    services = Column(String)
    rooms_quantity = Column(Integer)
    image_id = Column(Integer)
