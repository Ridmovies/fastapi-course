from app.booking.models import Booking
from app.service.base import BaseService


class BookingService(BaseService):
    model = Booking


