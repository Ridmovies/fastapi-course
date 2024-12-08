from fastapi import FastAPI, Depends
import uvicorn
from sqlalchemy import text

from app.database import get_session, init_models
from app.schemas import BookingSchema, HotelSearchArgs

app = FastAPI()


# @app.get("/{hotel_id}")
# async def get_hotels(
#     hotel_data: HotelSearchArgs = Depends(),
# ):
#     return {"message": "ok"}
#
#
# @app.post("/booking")
# async def booking(data: BookingSchema):
#     return {
#         "message": "ok",
#         "data": data
#     }


@app.get("/check-db-connection")
async def check_db_connection(session=Depends(get_session)):
    # Выполняем запрос к базе данных
    result = await session.execute(text("SELECT 1"))
    return {"message": "Connection to the database successful"}


@app.get("/init-db")
async def init_db():
    await init_models()
    return {"message": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

