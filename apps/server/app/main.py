from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload_routes import router as upload_router
from app.api.user_routes import router as user_router
from app.db.database import Base, engine

# Ensures tables are created when app starts.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Backend")

origins = [
    "http://localhost:5173",  # dev
    "https://playground-client-ruby.vercel.app",  # prod: Vercel
    "http://13.235.40.226:5173" # prod: AWS
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(upload_router)


@app.get("/")
def home() -> dict[str, str]:
    return {"msg": "Backend chal raha hai"}