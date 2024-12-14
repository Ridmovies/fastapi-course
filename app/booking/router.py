from datetime import date

from fastapi import APIRouter, Request, Depends
from sqlalchemy import select

from app.booking.models import Booking
from app.booking.schemas import BookingSchema, BookingInSchema
from app.booking.services import BookingService
from app.database import SessionDep
from app.users.dependencies import get_current_user_id
from app.users.models import User
from app.users.services import UserService

router = APIRouter()


@router.get("/", response_model=list[BookingSchema])
async def get_booking_list(
        request: Request,
        session: SessionDep,
        user_id: int = Depends(get_current_user_id)
):
    user: User = await UserService.get_one_by_id(user_id)
    print(f"user: {user}")
    bookings = await BookingService.get_all()
    return bookings


@router.get("/{booking_id}", response_model=BookingSchema)
async def get_booking(session: SessionDep, booking_id: int):
    booking = await BookingService.get_one_by_id(booking_id,)
    return booking


@router.post("/", response_model=BookingSchema | None)
async def create_booking(
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date):
    booking = await BookingService.add_booking_object(
        user_id,
        room_id,
        date_from,
        date_to,
    )

    return booking


