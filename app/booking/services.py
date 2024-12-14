from datetime import date

from fastapi.logger import logger
from sqlalchemy import select, and_, or_, func, insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.booking.models import Booking
from app.database import async_session
from app.exceptions import RoomCantBookedException
from app.rooms.models import Room
from app.service.base import BaseService


class BookingService(BaseService):
    model = Booking

    @classmethod
    async def add_booking_object(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date
    ):
        """Добавляет объект бронирования в БД."""
        try:
            async with async_session() as session:
                booked_rooms = select(Booking).where(
                    and_(
                        Booking.room_id == room_id,
                        or_(
                            and_(
                                Booking.date_from >= date_from,
                                Booking.date_from <= date_to
                            ),
                            and_(
                                Booking.date_from <= date_from,
                                Booking.date_to > date_from
                            )
                        )
                    )
                ).cte('booked_rooms')

                get_available_rooms = (
                    select(
                        (Room.quantity - func.count(booked_rooms.c.room_id))
                        .label('rooms_available')
                    )
                    .select_from(Room)
                    .join(
                        booked_rooms, booked_rooms.c.room_id == Room.id,
                        isouter=True
                    )
                    .where(Room.id == room_id)
                    .group_by(Room.quantity, booked_rooms.c.room_id)
                )

                rooms_available = await session.execute(get_available_rooms)
                rooms_available = rooms_available.scalar()

                if not rooms_available:
                    raise RoomCantBookedException

                get_room_price = select(
                    Room.price_per_day
                ).filter_by(id=room_id)

                price = await session.execute(get_room_price)
                price = price.scalar()

                add_booking = insert(Booking).values(
                    user_id=user_id,
                    room_id=room_id,
                    date_from=date_from,
                    date_to=date_to,
                    price_per_day=price
                ).returning(
                    Booking.id, Booking.date_from, Booking.date_to,
                    Booking.price, Booking.total_days,
                    Booking.total_cost, Booking.room_id,
                    Booking.user_id
                )

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.mappings().one()

        except RoomCantBookedException:
            raise RoomCantBookedException

        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                message = 'Database Exception'
            elif isinstance(error, Exception):
                message = 'Unknown Exception'
            message += ': Невозможно добавить бронирование'
            extra = {
                'user_id': user_id,
                'room_id': room_id,
                'date_from': date_from,
                'date_to': date_to,
            }
            logger.error(message, extra=extra, exc_info=True)

