# Playground

Full-stack monorepo for a React frontend and FastAPI backend.

## Stack

- Frontend: Vite + React (`apps/client`)
- Backend: FastAPI + Uvicorn (`apps/server`)
- Package manager: `pnpm`
- Database: SQLite
- File storage: AWS S3 for user image uploads

## Project Structure

```text
apps/
  client/   React app
  server/   FastAPI app
```

## Prerequisites

- Node.js
- `pnpm`
- Python 3

## Install

Install frontend workspace dependencies from the repo root:

```bash
pnpm install
```

Install backend dependencies inside `apps/server`:

```bash
pip install -r requirements.txt
```

## Run Locally

Start frontend and backend together from the repo root:

```bash
pnpm dev
```

Available root scripts:

- `pnpm dev` - starts client and server together
- `pnpm dev:client` - starts only the Vite frontend
- `pnpm dev:backend` - starts only the FastAPI backend
- `pnpm build` - builds the client and byte-compiles backend Python files

## Local URLs

- Frontend: `http://localhost:5173/`
- Backend: `http://127.0.0.1:8000/`

## Environment Variables

### Frontend

Set this in `apps/client/.env`:

- `VITE_API_URL=http://127.0.0.1:8000`

### Backend

The backend reads environment values from `apps/server/.env`.

Required for S3-backed image upload:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_BUCKET_NAME`

## Docker

This repo includes Docker Compose files for running both services in containers.

From the repo root:

```bash
docker compose up --build
```

## Database Note

The backend creates tables on startup with `Base.metadata.create_all()`.

If your SQLite database was created before the `image_url` column existed on `users`, you may need to:

- reset the SQLite database, or
- run an `ALTER TABLE` migration manually
