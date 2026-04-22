from fastapi import APIRouter, UploadFile, File
from app.services.s3 import upload_file

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file.file.seek(0)  # Reset file pointer if content was consumed
    url = upload_file(file)
    return {"url": url}