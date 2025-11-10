from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from typing import Optional


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, max_length=13)
    published_date: Optional[date] = None
    total_copies: int = Field(default=1, ge=1)
    available_copies: int = Field(default=1, ge=0)


class BookCreate(BookBase):
    author_id: int = Field(..., gt=0)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Harry Potter and the Philosopher's Stone",
                "author_id": 1,
                "isbn": "9780747532699",
                "published_date": "1997-06-26",
                "total_copies": 5,
                "available_copies": 5
            }
        }
    )


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, max_length=13)
    published_date: Optional[date] = None
    author_id: Optional[int] = Field(None, gt=0)
    total_copies: Optional[int] = Field(None, ge=1)
    available_copies: Optional[int] = Field(None, ge=0)


class BookResponse(BookBase):
    id: int
    author_id: int
    author_name: str 
    is_available: bool 
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class BookSearch(BaseModel):
    title: Optional[str] = None
    author_name: Optional[str] = None
    isbn: Optional[str] = None
    available_only: Optional[bool] = False
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)
