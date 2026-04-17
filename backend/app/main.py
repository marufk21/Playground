from fastapi import FastAPI

from app.api.user_routes import router as user_router
from app.db.database import Base, engine

# Ensures tables are created when app starts.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Backend")
app.include_router(user_router)


@app.get("/")
def home() -> dict[str, str]:
    return {"msg": "Backend chal raha hai"}