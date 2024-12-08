from fastapi import FastAPI
import uvicorn
from app.hotels.views import router as hotels_router


app = FastAPI()
app.include_router(hotels_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

