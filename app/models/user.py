from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):    
    __tablename__ = "users"  # Table name in database
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # User Information
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    # One user can borrow many books
    borrow_records = relationship(
        "BorrowRecord", 
        back_populates="user",
        cascade="all, delete-orphan"  # Delete records if user is deleted
    )
    
    def __repr__(self):
        return f"<User {self.username}>"
