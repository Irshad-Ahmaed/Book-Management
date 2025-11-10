from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import List, Tuple
from app.models.book import Book
from app.models.borrow import BorrowRecord, BorrowStatus
from app.models.user import User
from app.schemas.borrow import BorrowCreate


class BorrowService:
    @staticmethod
    def borrow_book(
        db: Session,
        user: User,
        borrow_data: BorrowCreate
    ) -> BorrowRecord:
        # Find book
        book = db.query(Book).filter(
            Book.id == borrow_data.book_id
        ).first()
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {borrow_data.book_id} not found"
            )
        
        # Check availability
        if book.available_copies <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book '{book.title}' is not available for borrowing"
            )
        
        # Check if user already has this book borrowed
        existing_borrow = db.query(BorrowRecord).filter(
            BorrowRecord.user_id == user.id,
            BorrowRecord.book_id == book.id,
            BorrowRecord.return_date == None  # Not returned yet
        ).first()
        
        if existing_borrow:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"You already have this book borrowed"
            )
        
        # Calculate due date
        due_date = datetime.utcnow() + timedelta(days=borrow_data.due_days)
        
        # Create borrow record
        borrow_record = BorrowRecord(
            user_id=user.id,
            book_id=book.id,
            due_date=due_date,
            status=BorrowStatus.BORROWED
        )
        
        # Decrement available copies
        book.available_copies -= 1
        
        # Save to database
        db.add(borrow_record)
        db.commit()
        db.refresh(borrow_record)
        
        return borrow_record
    
    @staticmethod
    def return_book(db: Session, record_id: int, user: User) -> BorrowRecord:
        # Find borrow record
        borrow_record = db.query(BorrowRecord).filter(
            BorrowRecord.id == record_id
        ).first()
        
        if not borrow_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Borrow record with id {record_id} not found"
            )
        
        # Verify user owns this borrow record
        if borrow_record.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to return this book"
            )
        
        # Check if already returned
        if borrow_record.return_date is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This book has already been returned"
            )
        
        # Mark as returned
        borrow_record.return_date = datetime.utcnow()
        
        # Update status (returned or overdue)
        if borrow_record.is_overdue:
            borrow_record.status = BorrowStatus.OVERDUE
        else:
            borrow_record.status = BorrowStatus.RETURNED
        
        # Increment available copies
        book = borrow_record.book
        book.available_copies += 1
        
        # Save changes
        db.commit()
        db.refresh(borrow_record)
        
        return borrow_record
    
    @staticmethod
    def get_user_borrow_history(
        db: Session,
        user: User,
        page: int = 1,
        page_size: int = 10,
        active_only: bool = False
    ) -> Tuple[List[BorrowRecord], int]:
        # Base query
        query = db.query(BorrowRecord).filter(
            BorrowRecord.user_id == user.id
        )
        
        # Filter for active only
        if active_only:
            query = query.filter(BorrowRecord.return_date == None)
        
        # Order by most recent first
        query = query.order_by(BorrowRecord.borrow_date.desc())
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        skip = (page - 1) * page_size
        records = query.offset(skip).limit(page_size).all()
        
        return records, total
    
    @staticmethod
    def check_overdue_books(db: Session) -> List[BorrowRecord]:
        # Find unreturned books past due date
        now = datetime.utcnow()
        
        overdue_records = db.query(BorrowRecord).filter(
            BorrowRecord.return_date == None,  # Not returned
            BorrowRecord.due_date < now,       # Past due date
            BorrowRecord.status != BorrowStatus.OVERDUE  # Not already marked
        ).all()
        
        # Update status to overdue
        for record in overdue_records:
            record.status = BorrowStatus.OVERDUE
        
        # Save changes
        if overdue_records:
            db.commit()
        
        return overdue_records


"""
Example: Calculate late fee
============================
return_date = datetime(2025, 11, 20)
due_date = datetime(2025, 11, 10)
days_late = (return_date - due_date).days  # 10 days
late_fee = days_late * 1.00  # $1 per day = $10
"""