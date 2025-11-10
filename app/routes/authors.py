from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List
from math import ceil

from app.database import get_db
from app.schemas.author import (
    AuthorCreate, 
    AuthorUpdate, 
    AuthorResponse, 
    AuthorWithBooks
)
from app.services.author import AuthorService
from app.utils.dependencies import get_current_active_user
from app.models.user import User

# Create router
router = APIRouter(
    prefix="/api/v1/authors",
    tags=["Authors"]
)


@router.post(
    "/",
    response_model=AuthorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new author"
)
def create_author(
    author_data: AuthorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    author = AuthorService.create_author(db, author_data)
    return author


@router.get(
    "/",
    response_model=dict,
    summary="List all authors"
)
def get_authors(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Calculate skip
    skip = (page - 1) * page_size
    authors, total = AuthorService.get_authors(db, skip, page_size)
    total_pages = ceil(total / page_size)
    
    # ✅ Convert each ORM object to Pydantic model
    author_list = [AuthorResponse.model_validate(author) for author in authors]
    
    # Calculate total pages
    total_pages = ceil(total / page_size)
    
    return {
        "authors": author_list,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.get(
    "/{author_id}",
    response_model=AuthorWithBooks,
    summary="Get author by ID"
)
def get_author(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    author = AuthorService.get_author_by_id(db, author_id)
    return author


@router.patch(
    "/{author_id}",
    response_model=AuthorResponse,
    summary="Update author"
)
def update_author(
    author_id: int,
    author_data: AuthorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    author = AuthorService.update_author(db, author_id, author_data)
    return author


@router.delete(
    "/{author_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete author"
)
def delete_author(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = AuthorService.delete_author(db, author_id)
    return result
