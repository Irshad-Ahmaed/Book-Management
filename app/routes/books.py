from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from math import ceil

from app.database import get_db
from app.schemas.book import (
    BookCreate,
    BookUpdate,
    BookResponse,
    BookSearch
)
from app.services.book import BookService
from app.utils.dependencies import get_current_active_user
from app.models.user import User

# Create router
router = APIRouter(
    prefix="/api/v1/books",
    tags=["Books"]
)


@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new book"
)
def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    book = BookService.create_book(db, book_data)
    
    # Add computed field for response
    book.author_name
    # book.is_available = book.available_copies > 0
    
    return book


@router.get(
    "/",
    response_model=dict,
    summary="List and search books"
)
def get_books(
    title: Optional[str] = Query(None, description="Search by title"),
    author_name: Optional[str] = Query(None, description="Search by author name"),
    isbn: Optional[str] = Query(None, description="Search by ISBN"),
    available_only: bool = Query(False, description="Show only available books"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Create search object
    search = BookSearch(
        title=title,
        author_name=author_name,
        isbn=isbn,
        available_only=available_only,
        page=page,
        page_size=page_size
    )
    
    # Get books
    books, total = BookService.get_books(db, search)
    
    # Add computed fields
    book_list = [BookResponse.model_validate(book) for book in books]
    
    # Calculate total pages
    total_pages = ceil(total / page_size)
    
    return {
        "books": book_list,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Get book by ID"
)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    book = BookService.get_book_by_id(db, book_id)
    
    # Add computed fields
    book.author_name
    # book.is_available = book.available_copies > 0
    
    return book

@router.patch(
    "/{book_id}",
    response_model=BookResponse,
    summary="Update book"
)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    book = BookService.update_book(db, book_id, book_data)
    
    # Add computed fields
    book.author_name
    # book.is_available = book.available_copies > 0
    
    return book

@router.delete(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete book"
)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = BookService.delete_book(db, book_id)
    return result