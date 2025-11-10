from app.routes.auth import router as auth_router
from app.routes.authors import router as authors_router
from app.routes.books import router as books_router
from app.routes.borrow import router as borrow_router

__all__ = [
    "auth_router",
    "authors_router", 
    "books_router",
    "borrow_router"
]