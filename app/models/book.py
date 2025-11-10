from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Book(Base):    
    __tablename__ = "books"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    title = Column(String(255), nullable=False, index=True)
    isbn = Column(String(13), unique=True, index=True, nullable=True)
    published_date = Column(Date, nullable=True)
    
    # Foreign Key (Links to Author)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    
    # Availability
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    # Many books belong to one author
    author = relationship("Author", back_populates="books")
    
    # One book can have many borrow records
    borrow_records = relationship(
        "BorrowRecord",
        back_populates="book",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Book {self.title}>"
    
    @property
    def is_available(self) -> bool:
        return self.available_copies > 0


"""
Understanding Foreign Keys:
===========================
ForeignKey links two tables together.

author_id = ForeignKey("authors.id")
     ↓
This book's author_id must match an id in the authors table

Example:
Authors table:
  id | name
  1  | J.K. Rowling
  2  | George R.R. Martin

Books table:
  id | title              | author_id
  1  | Harry Potter       | 1
  2  | Game of Thrones    | 2

Book 1's author_id (1) points to J.K. Rowling's id (1)
"""