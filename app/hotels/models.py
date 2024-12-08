from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Hotel(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[str]
    rooms_quantity: Mapped[int]
    image_id: Mapped[int]
