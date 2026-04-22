import os
from uuid import uuid4

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

BUCKET = os.getenv("AWS_BUCKET_NAME")


def upload_file(file):
    if not BUCKET:
        raise RuntimeError("AWS_BUCKET_NAME is not configured.")

    filename = f"{uuid4()}_{file.filename}"

    try:
        s3.upload_fileobj(
            file.file,
            BUCKET,
            filename,
            ExtraArgs={"ContentType": file.content_type},
        )
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError("Image upload failed.") from exc

    return f"https://{BUCKET}.s3.amazonaws.com/{filename}"
