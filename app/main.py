from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routes import (
    auth_router,
    authors_router,
    books_router,
    borrow_router
)

# Create FastAPI app instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="""
    📚 Library Management API
    
    A comprehensive book library management system with:
    * User authentication (JWT)
    * Author management
    * Book catalog with search
    * Borrowing system with due dates
    
    ## Authentication
    Most endpoints require authentication. Get your token from `/api/v1/auth/login`
    and use it in the `Authorization: Bearer <token>` header.
    """,
    docs_url="/docs",  # Swagger UI at /docs
    redoc_url="/redoc"  # ReDoc at /redoc
)


# Register Routes
app.include_router(auth_router)      # /api/v1/auth/*
app.include_router(authors_router)   # /api/v1/authors/*
app.include_router(books_router)     # /api/v1/books/*
app.include_router(borrow_router)    # /api/v1/borrow/*


# Startup Event
@app.on_event("startup")
async def startup_event():
    print(f"🚀 Starting {settings.APP_NAME} v{settings.VERSION}")
    print(f"📊 Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")
    print(f"📚 API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔐 Authentication enabled with JWT")


# Shutdown Event
@app.on_event("shutdown")
async def shutdown_event():
    print(f"👋 Shutting down {settings.APP_NAME}")


# Root Endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Library Management API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "operational"
    }


# Health Check Endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.VERSION
    }
