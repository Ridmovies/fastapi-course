from app.hotels.models import Hotel
from app.service.base import BaseService


class HotelService(BaseService):
    model = Hotel
