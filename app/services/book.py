from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from typing import List, Tuple
from app.models.book import Book
from app.models.author import Author
from app.schemas.book import BookCreate, BookUpdate, BookSearch


class BookService:
    
    @staticmethod
    def create_book(db: Session, book_data: BookCreate) -> Book:
        # Verify author exists
        author = db.query(Author).filter(
            Author.id == book_data.author_id
        ).first()
        
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with id {book_data.author_id} not found"
            )
        
        # Check ISBN uniqueness (if provided)
        if book_data.isbn:
            existing_book = db.query(Book).filter(
                Book.isbn == book_data.isbn
            ).first()
            
            if existing_book:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Book with ISBN {book_data.isbn} already exists"
                )
        
        # Create book
        new_book = Book(
            title=book_data.title,
            author_id=book_data.author_id,
            isbn=book_data.isbn,
            published_date=book_data.published_date,
            total_copies=book_data.total_copies,
            available_copies=book_data.available_copies
        )
        
        # Save to database
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        
        return new_book
    
    @staticmethod
    def get_books(
        db: Session,
        search: BookSearch
    ) -> Tuple[List[Book], int]:
       
        query = db.query(Book)
        
        # Apply filters
        if search.title:
            # Case-insensitive partial match
            query = query.filter(
                Book.title.ilike(f"%{search.title}%")
            )
        
        if search.author_name:
            # Join with Author table to search by author name
            query = query.join(Author).filter(
                Author.name.ilike(f"%{search.author_name}%")
            )
        
        if search.isbn:
            query = query.filter(Book.isbn == search.isbn)
        
        if search.available_only:
            query = query.filter(Book.available_copies > 0)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination
        skip = (search.page - 1) * search.page_size
        books = query.offset(skip).limit(search.page_size).all()
        
        return books, total
    
    @staticmethod
    def get_book_by_id(db: Session, book_id: int) -> Book:
        book = db.query(Book).filter(Book.id == book_id).first()
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
        
        return book
    
    @staticmethod
    def update_book(
        db: Session,
        book_id: int,
        book_data: BookUpdate
    ) -> Book:

        # Find book
        book = db.query(Book).filter(Book.id == book_id).first()
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
        
        # Get update data
        update_data = book_data.model_dump(exclude_unset=True)
        
        # Validate author_id if being updated
        if "author_id" in update_data:
            author = db.query(Author).filter(
                Author.id == update_data["author_id"]
            ).first()
            
            if not author:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Author with id {update_data['author_id']} not found"
                )
        
        # Validate ISBN if being updated
        if "isbn" in update_data and update_data["isbn"]:
            existing_book = db.query(Book).filter(
                Book.isbn == update_data["isbn"],
                Book.id != book_id  # Exclude current book
            ).first()
            
            if existing_book:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Book with ISBN {update_data['isbn']} already exists"
                )
        
        # Validate available_copies <= total_copies
        total = update_data.get("total_copies", book.total_copies)
        available = update_data.get("available_copies", book.available_copies)
        
        if available > total:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Available copies cannot exceed total copies"
            )
        
        # Apply updates
        for field, value in update_data.items():
            setattr(book, field, value)
        
        # Save changes
        db.commit()
        db.refresh(book)
        
        return book
    
    @staticmethod
    def delete_book(db: Session, book_id: int) -> dict:
        # Find book
        book = db.query(Book).filter(Book.id == book_id).first()
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
        
        # Check for active borrows
        active_borrows = [
            record for record in book.borrow_records 
            if record.return_date is None
        ]
        
        if active_borrows:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete book with active borrow records. All copies must be returned first."
            )
        
        # Delete book
        db.delete(book)
        db.commit()
        
        return {"message": "Book deleted successfully"}


"""
Understanding SQL Filters:
==========================

1. ilike (case-insensitive like)
   ==============================
   Book.title.ilike("%Harry%")
   Matches: "Harry Potter", "harry potter", "HARRY POTTER"
   
   % = wildcard (matches anything)
   %Harry% = contains "Harry" anywhere

2. filter vs filter_by
   ====================
   .filter(Book.title == "Harry")      # Use expressions
   .filter_by(title="Harry")           # Simple equality only

3. Joins
   ======
   query.join(Author)                  # Join tables
   .filter(Author.name == "Rowling")   # Filter on joined table
   
   SQL equivalent:
   SELECT * FROM books
   JOIN authors ON books.author_id = authors.id
   WHERE authors.name = 'Rowling'

4. Count before pagination
   ========================
   total = query.count()               # Get total results
   results = query.offset(10).limit(10).all()  # Then paginate
   
   Why? To calculate total pages for UI
"""