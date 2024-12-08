from typing import Optional

from fastapi import FastAPI, Depends
import uvicorn

from schemas import BookingSchema, HotelSearchArgs

app = FastAPI()


@app.get("/{hotel_id}")
async def get_hotels(
    hotel_data: HotelSearchArgs = Depends(),
):
    return {"message": "ok"}


@app.post("/booking")
async def booking(data: BookingSchema):
    return {
        "message": "ok",
        "data": data
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

