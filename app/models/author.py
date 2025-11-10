from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Author(Base):
    
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(255), nullable=False, index=True)
    bio = Column(Text, nullable=True) 
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    # One author can have many books
    books = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Author {self.name}>"


"""
Why separate Author and Book tables?
====================================
Instead of storing author name in each book (repetition),
we store author once and link books to it.

Example:
Author: J.K. Rowling (id=1)
Books: 
  - Harry Potter 1 (author_id=1)
  - Harry Potter 2 (author_id=1)
  - Harry Potter 3 (author_id=1)

Benefits:
- No duplicate data
- Easy to update author info once
- Can get all books by an author easily
"""