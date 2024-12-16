from fastapi import APIRouter, UploadFile, File
import shutil
from app.tasks.tasks import process_image

router = APIRouter()


@router.post("/upload")
async def upload_file(name: int, file: UploadFile):
    image_path = f"app/static/images/{name}.webp"
    with open(image_path, "wb+") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_image.delay(image_path)
    return {"message": "file uploaded"}