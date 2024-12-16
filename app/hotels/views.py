from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.database import init_models, get_session
from app.hotels.schemas import BookingSchema, HotelSearchArgs
from app.hotels.services import HotelService

router = APIRouter()


@router.get("/")
async def get_hotels():
    hotels = await HotelService.get_all()
    return hotels


# @router.get("/{hotel_id}")
# async def get_hotels(
#     hotel_data: HotelSearchArgs = Depends(),
# ):
#     return {"message": "ok"}
#
#
# @router.post("/booking")
# async def booking(data: BookingSchema):
#     return {
#         "message": "ok",
#         "data": data
#     }


@router.get("/check-db-connection")
async def check_db_connection(session=Depends(get_session)):
    # Выполняем запрос к базе данных
    result = await session.execute(text("SELECT 1"))
    return {"message": "Connection to the database successful"}


@router.get("/init-db")
async def init_db():
    await init_models()
    return {"message": "ok"}