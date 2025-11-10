from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from math import ceil

from app.database import get_db
from app.schemas.borrow import BorrowCreate, BorrowResponse
from app.services.borrow import BorrowService
from app.utils.dependencies import get_current_active_user
from app.models.user import User

# Create router
router = APIRouter(
    prefix="/api/v1/borrow",
    tags=["Borrowing"]
)


# Borrow a book
@router.post(
    "/",
    response_model=BorrowResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Borrow a book"
)
def borrow_book(
    borrow_data: BorrowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Borrow book
    borrow_record = BorrowService.borrow_book(db, current_user, borrow_data)
    
    # Add computed field
    # borrow_record.book_title = borrow_record.book.title
    
    return borrow_record

# Return a book
@router.post(
    "/return/{record_id}",
    response_model=BorrowResponse,
    summary="Return a borrowed book"
)
def return_book(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Return book
    borrow_record = BorrowService.return_book(db, record_id, current_user)
    
    # Add computed field
    # borrow_record.book_title = borrow_record.book.title
    
    return borrow_record

# View borrow history
@router.get(
    "/history",
    response_model=dict,
    summary="View borrowing history"
)
def get_borrow_history(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    active_only: bool = Query(False, description="Show only active borrows"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):

    # Get history
    records, total = BorrowService.get_user_borrow_history(
        db,
        current_user,
        page,
        page_size,
        active_only
    )
    
    # Add computed fields
    record_list = [BorrowResponse.model_validate(r) for r in records]
    
    # Calculate total pages
    total_pages = ceil(total / page_size)
    
    return {
        "records": record_list,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }
