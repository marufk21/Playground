from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "Backend chal raha hai 🚀"}

@app.get("/users")
def get_users():
    return {"users": ["Maruf", "Dev"]}