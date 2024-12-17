from datetime import date

from fastapi import APIRouter, Request, Depends
from pydantic import parse_obj_as, TypeAdapter
from sqlalchemy import select

from app.booking.models import Booking
from app.booking.schemas import BookingSchema, BookingInSchema, BookingOutSchema
from app.booking.services import BookingService
from app.config import settings
from app.database import SessionDep
from app.users.dependencies import get_current_user_id, get_current_user
from app.users.models import User
from app.users.services import UserService

from app.tasks.tasks import send_booking_confirmation_email

router = APIRouter()


@router.get("", response_model=list[BookingSchema])
async def get_booking_list(
    request: Request, session: SessionDep, user_id: int = Depends(get_current_user_id)
):
    user: User = await UserService.get_one_by_id(user_id)
    bookings = await BookingService.get_all()
    return bookings


@router.get("/{booking_id}", response_model=BookingSchema)
async def get_booking(session: SessionDep, booking_id: int):
    booking = await BookingService.get_one_by_id(
        booking_id,
    )
    return booking


@router.post("", response_model=BookingOutSchema)
async def create_booking(
    # user_id: int,
    room_id: int,
    date_from: date,
    date_to: date,
    user: User = Depends(get_current_user),
):

    booking = await BookingService.create(
        user_id=user.id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
    )
    return booking
