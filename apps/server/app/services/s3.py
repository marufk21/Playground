import os
from uuid import uuid4

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION,
)

BUCKET = os.getenv("AWS_BUCKET_NAME")


def upload_file(file):
    if not BUCKET:
        raise RuntimeError("AWS_BUCKET_NAME is not configured.")
    if not AWS_REGION:
        raise RuntimeError("AWS_REGION is not configured.")

    filename = f"{uuid4()}_{file.filename}"
    file.file.seek(0)

    try:
        s3.upload_fileobj(
            file.file,
            BUCKET,
            filename,
            ExtraArgs={"ContentType": file.content_type},
        )
    except (BotoCoreError, ClientError, Exception) as exc:
        print(f"S3 upload failed: {exc!r}")
        raise

    return f"https://{BUCKET}.s3.{AWS_REGION}.amazonaws.com/{filename}"
