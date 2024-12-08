from datetime import date
from typing import Optional

from fastapi.params import Query
from pydantic import BaseModel


class BookingSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class HotelSearchArgs:
    def __init__(
            self,
            hotel_id: int,
            location: str,
            spa: Optional[bool] = None,
            stars: Optional[int] = Query(None, ge=1, le=5),
    ):
        self.hotel_id = hotel_id
        self.location = location
        self.spa = spa
        self.stars = stars