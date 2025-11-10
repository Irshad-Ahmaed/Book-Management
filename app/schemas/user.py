from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john@example.com",
                "username": "john_doe",
                "password": "SecurePass123!"
            }
        }
    )


class UserLogin(BaseModel):
    username: str
    password: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "john_doe",
                "password": "SecurePass123!"
            }
        }
    )


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    # from_attributes=True allows creating from SQLAlchemy models


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None