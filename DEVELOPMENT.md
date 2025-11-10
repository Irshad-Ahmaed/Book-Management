# 📝 Development Journey

## What challenges did I face while building this?

### Challenge 1: Understanding Alembic Migrations
**Problem**: 
Initially, I was confused about when to use Alembic vs `Base.metadata.create_all()`. I also forgot to import models in `alembic/env.py`, causing migrations to skip tables.

**Solution**:
- Learned that Alembic is the professional way for production
- Created a checklist: always import ALL models in env.py
- Practiced creating and rolling back migrations

**Learning**: Database migrations are like Git for your database schema!

---

### Challenge 2: Relationships in SQLAlchemy
**Problem**:
Got confused about `back_populates`, foreign keys, and how to access related data (like book.author.name).

**Solution**:
- Studied the relationship diagrams: User ↔ BorrowRecord ↔ Book ↔ Author
- Practiced querying with relationships in Python shell
- Understood that relationships are just shortcuts for joins

**Learning**: Relationships make code cleaner but need to understand the underlying SQL!

---

## How did I solve them?

1. **Read Documentation**: FastAPI and SQLAlchemy docs are excellent
2. **Took Help From AI**: used various AI to learn it. 
3. **Drew Diagrams**: Visualized relationships and data flow
6. **Asked Questions**: When stuck, broke down the problem into smaller questions

---

## What would I do differently if I had more time?

1. **Testing**: Add unit tests and integration tests using pytest
2. **Error Handling**: Create custom exception handlers for better error messages
3. **Logging**: Add proper logging throughout the application
4. **Rate Limiting**: Prevent API abuse with rate limiting
5. **Caching**: Add Redis for caching frequently accessed data
---

## What did I learn from this assignment?

### Technical Skills

1. **FastAPI Mastery**:
   - Dependency injection system
   - Automatic API documentation
   - Request validation with Pydantic
   - JWT authentication

2. **Database Design**:
   - Proper table relationships
   - Foreign keys and constraints
   - Indexes for performance
   - Migration management with Alembic

3. **API Design**:
   - RESTful principles
   - Proper status codes
   - Pagination strategies
   - Search and filtering

4. **Security**:
   - Password hashing (never store plain!)
   - JWT token lifecycle
   - Protected endpoints
   - CORS configuration

### Soft Skills

1. **Problem Decomposition**: Breaking large problems into smaller, manageable pieces
2. **Documentation**: Writing clear explanations and examples
3. **Code Organization**: Structuring projects for maintainability
4. **Testing Mindset**: Thinking about edge cases and validation
