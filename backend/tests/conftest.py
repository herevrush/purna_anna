import os
import sys
import uuid as _uuid

# Set required env vars before any app imports
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-only")

# Add backend dir to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Patch PostgreSQL UUID for SQLite BEFORE importing app models
from sqlalchemy.types import TypeDecorator, CHAR
import sqlalchemy.dialects.postgresql as _pg_dialect


class SQLiteUUID(TypeDecorator):
    impl = CHAR(36)
    cache_ok = True

    def __init__(self, as_uuid=True, **kwargs):
        self.as_uuid = as_uuid
        super().__init__(**kwargs)

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if self.as_uuid:
            return _uuid.UUID(str(value))
        return value


_pg_dialect.UUID = SQLiteUUID

# Now import app modules (after patch)
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.db.base import Base
from app.core.deps import get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def clean_tables():
    yield
    with engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def admin_token(client, db):
    from app.models.user import User
    from app.core.security import get_password_hash
    user = User(
        email="admin@test.com",
        hashed_password=get_password_hash("adminpass"),
        is_admin=True,
    )
    db.add(user)
    db.commit()
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@test.com", "password": "adminpass"},
    )
    return response.json()["access_token"]


@pytest.fixture
def user_token(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "user@test.com", "password": "userpass"},
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "user@test.com", "password": "userpass"},
    )
    return response.json()["access_token"]
