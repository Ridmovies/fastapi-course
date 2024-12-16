from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import text

from app.database import init_models, get_session
from app.hotels.schemas import HotelSchema
from app.hotels.services import HotelService

router = APIRouter()


@router.get("/", response_model=list[HotelSchema])
@cache(expire=30)
async def get_hotels():
    hotels = await HotelService.get_all()
    return hotels


@router.get("/check-db-connection")
async def check_db_connection(session=Depends(get_session)):
    # Выполняем запрос к базе данных
    result = await session.execute(text("SELECT 1"))
    return {"message": "Connection to the database successful"}


@router.get("/init-db")
async def init_db():
    await init_models()
    return {"message": "ok"}