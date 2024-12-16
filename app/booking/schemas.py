from datetime import datetime, date

from pydantic import BaseModel


class BookingInSchema(BaseModel):
    date_from: date
    date_to: date
    price: int
    room_id: int
    user_id: int

    class Config:
        from_attributes = True


class BookingSchema(BaseModel):
    id: int
    price: int
    total_days: int
    total_cost: int
    room_id: int
    user_id: int

    class Config:
        from_attributes = True


class BookingOutSchema(BaseModel):
    test: str
