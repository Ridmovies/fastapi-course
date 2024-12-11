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
    user: User = await UserService.get_one_by_id(session, user_id)
    print(f"user: {user}")
    bookings = await BookingService.get_all(session)
    return bookings


@router.get("/{booking_id}", response_model=BookingSchema)
async def get_booking(session: SessionDep, booking_id: int):
    booking = await BookingService.get_one_by_id(booking_id, session)
    return booking


@router.post("/", response_model=BookingSchema)
async def create_booking(
    session: SessionDep,
    booking: BookingInSchema,
):
    booking = Booking(**booking.model_dump())
    session.add(booking)
    await session.commit()
    # booking = await BookingService.create(session, booking)
    return booking

