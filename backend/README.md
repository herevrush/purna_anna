# Purna Grocery API

A production-ready FastAPI backend for the Purna online grocery store.

## Features

- JWT authentication (register, login, protected routes)
- Product catalog with category filtering and pagination
- Shopping cart (add, update, remove items)
- Order checkout (cart → order conversion)
- Alembic database migrations
- PostgreSQL via SQLAlchemy 2.0

## Prerequisites

- Python 3.11+
- PostgreSQL (running locally or via Docker)

## Setup

```bash
# 1. Clone and enter the backend directory
cd backend

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL and a strong SECRET_KEY

# 5. Run database migrations
alembic upgrade head

# 6. Start the development server
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

## API Documentation

Interactive Swagger UI: http://localhost:8000/docs  
ReDoc: http://localhost:8000/redoc  
Health check: http://localhost:8000/health

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | — | PostgreSQL connection string |
| `SECRET_KEY` | — | JWT signing secret (change in production!) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | JWT token lifetime |

## Project Structure

```
backend/
  app/
    api/v1/endpoints/   # Route handlers (users, products, categories, cart, orders)
    core/               # Config, security (JWT/bcrypt), dependency injection
    db/                 # SQLAlchemy engine, session factory, declarative base
    models/             # ORM models (User, Product, Category, CartItem, Order, OrderItem)
    schemas/            # Pydantic request/response schemas
    services/           # Business logic layer (extensible)
  alembic/              # Database migration scripts
  main.py               # FastAPI application entry point
  requirements.txt
  .env.example
```

## Running Migrations

```bash
# Generate a new migration after model changes
alembic revision --autogenerate -m "describe your change"

# Apply all pending migrations
alembic upgrade head

# Roll back one migration
alembic downgrade -1
```
