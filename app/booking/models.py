from datetime import datetime

from sqlalchemy import Date, ForeignKey, Integer, Computed
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    date_from: Mapped[datetime] = mapped_column(Date, nullable=False)
    date_to: Mapped[datetime] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(nullable=False, default=100)
    total_days: Mapped[int] = mapped_column(
        Integer, Computed('date_to - date_from + 1'), nullable=False
    )
    total_cost: Mapped[int] = mapped_column(
        Integer, Computed('(date_to - date_from + 1) * price'),
        nullable=False
    )
    # room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    # user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    # user = relationship('User', back_populates='booking')
    # room = relationship('Room', back_populates='booking')