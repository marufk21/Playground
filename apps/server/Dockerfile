# Python base image
FROM python:3.11-slim

# Build arguments for environment variables
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_BUCKET_NAME
ARG AWS_REGION
ARG DATABASE_URL

# Set environment variables from build args
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV AWS_BUCKET_NAME=${AWS_BUCKET_NAME}
ENV AWS_REGION=${AWS_REGION}
ENV DATABASE_URL=${DATABASE_URL}

# Working directory
WORKDIR /app

# Copy requirements first (cache optimization)
COPY requirements.txt .

# Some Windows editors can save `requirements.txt` as UTF-16 (null-byte separated),
# which `pip` can't parse. Normalize to UTF-8/ASCII bytes before installing.
RUN python -c "from pathlib import Path; p=Path('requirements.txt'); b=p.read_bytes(); p.write_bytes(b.replace(b'\\x00', b''))"

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]