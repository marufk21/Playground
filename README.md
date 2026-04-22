# Playground

Monorepo dev setup:
- **Frontend**: Vite + React (workspace app: `apps/client`)
- **Backend**: FastAPI (Uvicorn, `apps/server`)

## Setup

```bash
pnpm install
```

## Run (frontend + backend)

```bash
pnpm dev
```

## URLs

- **Frontend**: `http://localhost:5173/`
- **Backend**: `http://127.0.0.1:8000/`

## User image upload (S3)

Backend expects these env vars (see `apps/server/app/services/s3.py`):

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_BUCKET_NAME`

Frontend should set:

- `VITE_API_URL` (e.g. `http://127.0.0.1:8000`)

### DB note (SQLite)

The backend uses `Base.metadata.create_all()` on startup; if you already created the `users` table before adding `image_url`, you may need to reset your SQLite DB (or run an `ALTER TABLE` to add the column).
