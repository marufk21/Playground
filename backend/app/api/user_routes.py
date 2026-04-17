from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, get_users

router = APIRouter(tags=["Users"])


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    try:
        return create_user(db=db, user_data=user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists.",
        ) from None


@router.get("/users", response_model=list[UserResponse])
def get_users_route(db: Session = Depends(get_db)) -> list[UserResponse]:
    return get_users(db=db)
