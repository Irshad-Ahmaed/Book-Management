# 📚 Library Management API

A comprehensive FastAPI-based library management system with user authentication, book catalog management, and borrowing functionality.

## 🎯 Features

- ✅ User Authentication (JWT-based)
- ✅ Author Management (CRUD operations)
- ✅ Book Catalog (CRUD with search/filter)
- ✅ Borrowing System (borrow, return, history)
- ✅ Pagination support
- ✅ PostgreSQL database (Neon)
- ✅ Alembic migrations
- ✅ API documentation (Swagger UI)

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL (Neon)
- **ORM**: SQLAlchemy 2.0.25
- **Migrations**: Alembic 1.13.1
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **Validation**: Pydantic 2.5.3

## 📋 Prerequisites

- Python 3.9 or higher
- PostgreSQL database (Neon account)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Irshad-Ahmaed/Book-Management.git
cd Book-Management
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your values:
# - DATABASE_URL (from Neon dashboard)
# - SECRET_KEY (generate using: python -c "import secrets; print(secrets.token_hex(32))")
```

### 5. Initialize Database
```bash
# Create initial migration
alembic revision --autogenerate -m "Initial tables"

# Apply migrations to database
alembic upgrade head
```

### 6. Run the Application
```bash
# Using run.py
python run.py

# OR using uvicorn directly
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

## 📖 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication

Most endpoints require authentication. Here's how to use them:

### 1. Register a User
```bash
POST http://localhost:8000/api/v1/auth/register
Content-Type: application/json

{
  "email": "john@example.com",
  "username": "john_doe",
  "password": "SecurePass123!"
}
```

### 2. Login
```bash
POST http://localhost:8000/api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=SecurePass123!
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Use Token in Requests

Add the token to the Authorization header:
```bash
GET http://localhost:8000/api/v1/books
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Authors (Protected)
- `POST /api/v1/authors` - Create author
- `GET /api/v1/authors` - List authors (paginated)
- `GET /api/v1/authors/{id}` - Get author details
- `PATCH /api/v1/authors/{id}` - Update author
- `DELETE /api/v1/authors/{id}` - Delete author

### Books (Protected)
- `POST /api/v1/books` - Create book
- `GET /api/v1/books` - List/search books (paginated)
- `GET /api/v1/books/{id}` - Get book details
- `PATCH /api/v1/books/{id}` - Update book
- `DELETE /api/v1/books/{id}` - Delete book

### Borrowing (Protected)
- `POST /api/v1/borrow` - Borrow a book
- `POST /api/v1/borrow/return/{record_id}` - Return a book
- `GET /api/v1/borrow/history` - View borrow history

## 🧪 Example API Calls

### Using cURL
```bash
# Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","username":"john_doe","password":"SecurePass123!"}'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=SecurePass123!"

# Create Author (with token)
curl -X POST "http://localhost:8000/api/v1/authors" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"name":"J.K. Rowling","bio":"British author"}'

# Search Books
curl -X GET "http://localhost:8000/api/v1/books?title=Harry&available_only=true" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```