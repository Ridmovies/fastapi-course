from fastapi import APIRouter, UploadFile, File
import shutil

router = APIRouter()


@router.post("/upload")
async def upload_file(name: int, file: UploadFile):
    with open(f"app/static/images/{name}.webp", "wb+") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "file uploaded"}