# ADR: Backend Architecture — Purna Grocery Store API

**Author:** Danny (Tech Lead)  
**Date:** 2025-01-01  
**Status:** Accepted

---

## Context

We are building the backend for a grocery store app. The frontend is a separate Next.js app. The backend needs to handle products, categories, cart, orders, and user accounts.

---

## Decisions

### 1. Folder Layout

```
backend/
├── alembic/                  # Migration scripts
│   └── versions/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py     # Mounts all sub-routers
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── products.py
│   │       ├── categories.py
│   │       ├── cart.py
│   │       └── orders.py
│   ├── core/
│   │   ├── config.py         # Settings via pydantic-settings
│   │   ├── security.py       # JWT encode/decode, password hashing
│   │   └── dependencies.py   # get_db, get_current_user
│   ├── db/
│   │   ├── base.py           # SQLAlchemy declarative base
│   │   └── session.py        # engine + SessionLocal
│   ├── models/               # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── cart.py
│   │   └── order.py
│   ├── schemas/              # Pydantic request/response schemas
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── cart.py
│   │   └── order.py
│   ├── services/             # Business logic layer
│   │   ├── user_service.py
│   │   ├── product_service.py
│   │   ├── cart_service.py
│   │   └── order_service.py
│   └── main.py               # FastAPI app factory, mounts /api/v1
├── tests/
│   ├── conftest.py
│   └── test_*.py
├── alembic.ini
├── pyproject.toml
└── .env.example
```

### 2. Key Libraries

| Library | Purpose |
|---|---|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `sqlalchemy` | ORM |
| `alembic` | DB migrations |
| `pydantic` + `pydantic-settings` | Schemas + config |
| `python-jose[cryptography]` | JWT tokens |
| `passlib[bcrypt]` | Password hashing |
| `psycopg2-binary` | PostgreSQL driver |
| `pytest` + `httpx` | Testing |

### 3. API Versioning

All routes are mounted under `/api/v1/`. If we break compatibility later, we add `/api/v2/` alongside it.

```
/api/v1/auth/login
/api/v1/auth/register
/api/v1/users/me
/api/v1/products/
/api/v1/categories/
/api/v1/cart/
/api/v1/orders/
```

### 4. Auth (JWT)

- `POST /api/v1/auth/register` — create account, return tokens
- `POST /api/v1/auth/login` — return `access_token` + `refresh_token`
- Access token: 30 min TTL, Bearer token in `Authorization` header
- Refresh token: 7 day TTL, stored in DB for rotation/revocation
- `get_current_user` dependency injected into protected routes via `Depends()`

### 5. Database Conventions

- SQLAlchemy `DeclarativeBase` in `app/db/base.py`
- All models import from `app/db/base.py`
- `alembic/env.py` imports all models so autogenerate works
- Migrations run via `alembic upgrade head`
- Never edit migration files after they've been committed — always create a new one

### 6. Domain Entities

**User** — id, email, hashed_password, full_name, is_active, is_admin, created_at

**Category** — id, name, slug, description, parent_id (self-referential for subcategories)

**Product** — id, name, slug, description, price, stock_quantity, category_id, image_url, is_active, created_at

**Cart** — id, user_id, created_at  
**CartItem** — id, cart_id, product_id, quantity

**Order** — id, user_id, status (pending/confirmed/shipped/delivered/cancelled), total_amount, created_at  
**OrderItem** — id, order_id, product_id, quantity, unit_price (snapshot at time of order)

### 7. Service Layer Convention

- Routers handle HTTP: parse input, call service, return response schema
- Services handle business logic: validation, DB queries, side effects
- Services receive a `db: Session` argument — no global state
- No SQLAlchemy queries in routers

### 8. Config

All config via environment variables, loaded with `pydantic-settings` in `app/core/config.py`:

```
DATABASE_URL=postgresql://user:pass@localhost/purna
SECRET_KEY=<strong-random-key>
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

`.env.example` ships with the repo. `.env` is gitignored.

---

## Consequences

- Linus scaffolds `backend/` following this layout exactly
- Basher wires CI to run `pytest` from `backend/` and `alembic check` to catch unapplied migrations
- All future backend PRs must keep routers thin (no business logic) and services stateless
