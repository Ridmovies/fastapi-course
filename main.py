import time
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI, version

from app.admin.auth import authentication_backend
from app.admin.views import BookingAdmin, HotelAdmin, UserAdmin
from app.booking.router import router as bookings_router
from app.config import settings
from app.database import async_engine
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router
from app.logger import logger
from app.pages.router import router as pages_router
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(hotels_router, prefix="/hotels", tags=["hotels"])
app.include_router(users_router, prefix="/users")
app.include_router(bookings_router, prefix="/booking", tags=["booking"])
app.include_router(pages_router, prefix="/pages", tags=["pages"])
app.include_router(images_router, prefix="/images", tags=["images"])

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@cache()
async def get_cache():
    return 1


@app.get("/")
@cache(expire=60)
async def index():
    return dict(hello="world")


@app.get("/")
async def root():
    return {"message": "Tomato"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Добавляет заголовок со временем выполнения запроса."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={"process_time": round(process_time, 4)})
    return response


app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/v{major}",
    # description='Greet users with a nice message',
    # middleware=[
    #     Middleware(SessionMiddleware, secret_key='mysecretkey')
    # ]
)

admin = Admin(app, async_engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(HotelAdmin)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
