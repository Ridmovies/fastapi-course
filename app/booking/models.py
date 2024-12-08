from sqlalchemy import Date, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Hotel(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(foreign_key='rooms.id')
    user_id: Mapped[int] = mapped_column(foreign_key='users.id')
    date_from: Mapped[Date] = mapped_column(nullable=False)
    date_to: Mapped[Date] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_days: Mapped[int] = mapped_column(
        computed=(func.date_part('day', date_to - date_from) + 1),
    )
    total_cost = mapped_column(
        computed=(func.date_part('day', date_to - date_from) + 1) * price,
        type_=Numeric(precision=8, scale=2),
        onupdate='IGNORE',
    )
