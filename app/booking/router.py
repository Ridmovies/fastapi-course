from datetime import date

from fastapi_versioning import version
from fastapi import APIRouter, Depends, Request
from app.booking.schemas import BookingOutSchema, BookingSchema
from app.booking.services import BookingService
from app.database import SessionDep
from app.users.dependencies import get_current_user, get_current_user_id
from app.users.models import User

router = APIRouter()


@router.get("", response_model=list[BookingSchema])
@version(1)
async def get_booking_list(user: User = Depends(get_current_user)):
    bookings = await BookingService.get_all()
    return bookings


@router.get("/{booking_id}", response_model=BookingSchema)
@version(1)
async def get_booking(session: SessionDep, booking_id: int):
    booking = await BookingService.get_one_by_id(
        booking_id,
    )
    return booking


@router.post("", response_model=BookingOutSchema)
@version(2)
async def create_booking(
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
