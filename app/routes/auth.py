"""
Authentication Routes
=====================
Handles user registration and login endpoints.

Endpoints:
- POST /api/v1/auth/register - Register new user
- POST /api/v1/auth/login    - Login user
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.auth import AuthService
from app.utils.security import create_access_token
from app.config import settings

# Create router
# APIRouter groups related endpoints together
router = APIRouter(
    prefix="/api/v1/auth",  # All routes start with /api/v1/auth
    tags=["Authentication"]  # Groups in API documentation
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # Call service to create user
    user = AuthService.create_user(db, user_data)
    return user


@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Authenticate user
    user = AuthService.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    # Create access token
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,  # "sub" is JWT standard for subject
            "user_id": user.id
        },
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
