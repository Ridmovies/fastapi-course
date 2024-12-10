from app.booking.models import Bookings
from app.service.base import BaceService


class BookingService(BaceService):
    model = Bookings


