from sqladmin import ModelView

from app.booking.models import Booking
from app.hotels.models import Hotel
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]


class BookingAdmin(ModelView, model=Booking):
    column_list = "__all__"


class HotelAdmin(ModelView, model=Hotel):
    column_list = "__all__"
