from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Tuple
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate


class AuthorService:
    
    @staticmethod
    def create_author(db: Session, author_data: AuthorCreate) -> Author:

        new_author = Author(
            name=author_data.name,
            bio=author_data.bio
        )
        
        # Save to database
        db.add(new_author)
        db.commit()
        db.refresh(new_author)
        
        return new_author
    
    @staticmethod
    def get_authors(
        db: Session, 
        skip: int = 0, 
        limit: int = 10
    ) -> Tuple[List[Author], int]:

        # Get total count
        total = db.query(Author).count()
        
        # Get paginated results
        authors = db.query(Author)\
            .offset(skip)\
            .limit(limit)\
            .all()
        
        return authors, total
    
    @staticmethod
    def get_author_by_id(db: Session, author_id: int) -> Author:
        author = db.query(Author).filter(Author.id == author_id).first()
        
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with id {author_id} not found"
            )
        
        return author
    
    @staticmethod
    def update_author(
        db: Session, 
        author_id: int, 
        author_data: AuthorUpdate
    ) -> Author:
        
        author = db.query(Author).filter(Author.id == author_id).first()
        
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with id {author_id} not found"
            )
        
        # Update only provided fields
        update_data = author_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(author, field, value)
        
        # Save changes
        db.commit()
        db.refresh(author)
        
        return author
    
    @staticmethod
    def delete_author(db: Session, author_id: int) -> dict:
        # Find author
        author = db.query(Author).filter(Author.id == author_id).first()
        
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with id {author_id} not found"
            )
        
        # Check if author has books
        if author.books:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete author with existing books. Delete or reassign books first."
            )
        
        # Delete author
        db.delete(author)
        db.commit()
        
        return {"message": "Author deleted successfully"}
