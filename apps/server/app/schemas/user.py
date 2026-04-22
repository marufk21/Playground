from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    image_url: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    image_url: str | None = None

    model_config = {"from_attributes": True}
