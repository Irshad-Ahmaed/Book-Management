from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timedelta
import enum
from app.database import Base


class BorrowStatus(str, enum.Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"
    OVERDUE = "overdue"


class BorrowRecord(Base):    
    __tablename__ = "borrow_records"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    
    # Dates
    borrow_date = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    due_date = Column(DateTime(timezone=True), nullable=False)
    return_date = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    status = Column(
        Enum(BorrowStatus),
        default=BorrowStatus.BORROWED,
        nullable=False
    )
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # Relationships
    user = relationship("User", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")
    
    def __repr__(self):
        return f"<BorrowRecord User:{self.user_id} Book:{self.book_id}>"
    
    @property
    def is_overdue(self) -> bool:
        if self.return_date:  # Already returned
            return False
        return datetime.now() > self.due_date


"""
Understanding Relationships:
============================

User ←→ BorrowRecord ←→ Book

user.borrow_records → List of all books user borrowed
book.borrow_records → List of all times book was borrowed

Example Query:
user = db.query(User).filter(User.id == 1).first()
borrowed_books = user.borrow_records  # All books this user borrowed

for record in borrowed_books:
    print(record.book.title)  # Access book through relationship
"""