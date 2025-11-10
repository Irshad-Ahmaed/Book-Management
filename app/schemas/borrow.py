from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.borrow import BorrowStatus


class BorrowCreate(BaseModel):
    book_id: int = Field(..., gt=0)
    due_days: int = Field(default=14, ge=1, le=90)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "book_id": 1,
                "due_days": 14
            }
        }
    )


class BorrowResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    book_title: str 
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: BorrowStatus
    is_overdue: bool 
    
    model_config = ConfigDict(from_attributes=True)


class BorrowHistory(BaseModel):
    records: list[BorrowResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
