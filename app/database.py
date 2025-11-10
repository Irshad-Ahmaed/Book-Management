"""
Database Connection
===================
Sets up SQLAlchemy connection to Neon PostgreSQL.

Components:
- Engine: Connection to database
- SessionLocal: Creates database sessions
- Base: Base class for all models
- get_db: Dependency for routes
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings


# Create database engine
# engine = like a "connection pool" to the database
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,      # Check connection health before using
    echo=settings.DEBUG,     # Log SQL queries when DEBUG=True
    pool_size=5,             # Number of connections to maintain
    max_overflow=10          # Max additional connections when needed
)

# Create SessionLocal class
# Session = a "conversation" with the database
SessionLocal = sessionmaker(
    autocommit=False,   # We manually control when to save
    autoflush=False,    # We manually control when to sync
    bind=engine         # Bind to our database engine
)

# Create Base class for models
# All models (User, Book, etc.) will inherit from this
Base = declarative_base()


def get_db():
    """
    Database Dependency
    ===================
    Provides database session to routes.
    FastAPI automatically calls this and injects db.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.models import user, author, book, borrow  # Import all models
    Base.metadata.create_all(bind=engine)