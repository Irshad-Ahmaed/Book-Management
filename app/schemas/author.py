from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    bio: Optional[str] = Field(None, max_length=5000)


class AuthorCreate(AuthorBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "J.K. Rowling",
                "bio": "British author, best known for Harry Potter series"
            }
        }
    )


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    bio: Optional[str] = Field(None, max_length=5000)


class AuthorResponse(AuthorBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Import here to avoid circular import
from app.schemas.book import BookResponse


class AuthorWithBooks(AuthorResponse):
    books: List[BookResponse] = []

    model_config = ConfigDict(from_attributes=True)
