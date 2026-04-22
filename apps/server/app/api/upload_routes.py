from fastapi import APIRouter, HTTPException, UploadFile, File, status
from app.services.s3 import upload_file

router = APIRouter()


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image uploads are allowed.",
        )

    file.file.seek(0)
    try:
        url = upload_file(file)
    except Exception as exc:
        print(f"Upload route failed: {exc!r}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {exc!r}",
        ) from exc

    return {"url": url}
