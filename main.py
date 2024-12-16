from contextlib import asynccontextmanager
from typing import AsyncIterator


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis

from app.admin.views import UserAdmin, BookingAdmin, HotelAdmin
from app.database import async_engine
from app.hotels.router import router as hotels_router
from app.users.router import router as users_router
from app.booking.router import router as bookings_router
from app.pages.router import router as pages_router
from app.images.router import router as images_router

from app.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(lifespan=lifespan)

admin = Admin(app, async_engine)
admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(HotelAdmin)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(hotels_router, prefix="/hotels", tags=["hotels"])
app.include_router(users_router, prefix="/users")
app.include_router(bookings_router, prefix="/booking", tags=["booking"])
app.include_router(pages_router, prefix="/pages", tags=["pages"])
app.include_router(images_router, prefix="/images", tags=["images"])

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=[
        'Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers',
        'Access-Control-Allow-Origin', 'Authorization'
    ],
)

@cache()
async def get_cache():
    return 1


@app.get("/")
@cache(expire=60)
async def index():
    return dict(hello="world")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

