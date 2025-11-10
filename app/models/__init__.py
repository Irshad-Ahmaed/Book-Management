"""
Imports all models for easy access.
"""

from app.models.user import User
from app.models.author import Author
from app.models.book import Book
from app.models.borrow import BorrowRecord

__all__ = ["User", "Author", "Book", "BorrowRecord"]