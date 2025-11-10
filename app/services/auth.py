from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash, verify_password


class AuthService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        existing_email = db.query(User).filter(
            User.email == user_data.email
        ).first()
        
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username already exists
        existing_username = db.query(User).filter(
            User.username == user_data.username
        ).first()
        
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        hashed_password = get_password_hash(user_data.password)
        
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            is_active=True
        )
        
        # Add to database
        db.add(new_user)
        db.commit() 
        db.refresh(new_user)  # Get the ID and timestamps
        
        return new_user
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        # Find user by username
        user = db.query(User).filter(User.username == username).first()
        
        # User doesn't exist
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if account is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account is inactive"
            )
        
        return user
