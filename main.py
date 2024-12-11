from fastapi import FastAPI
import uvicorn
from app.hotels.views import router as hotels_router
from app.users.router import router as users_router
from app.booking.router import router as bookings_router


app = FastAPI()
app.include_router(hotels_router, prefix="/hotels")
app.include_router(users_router, prefix="/users")
app.include_router(bookings_router, prefix="/booking", tags=["booking"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

