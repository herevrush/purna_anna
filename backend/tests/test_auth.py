def test_register(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "newuser@example.com", "password": "password123", "full_name": "New User"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "id" in data
    assert data["is_admin"] is False


def test_register_duplicate_email(client):
    payload = {"email": "dup@example.com", "password": "pass123"}
    client.post("/api/v1/auth/register", json=payload)
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400


def test_login_success(client):
    client.post("/api/v1/auth/register", json={"email": "login@example.com", "password": "pass123"})
    response = client.post("/api/v1/auth/login", data={"username": "login@example.com", "password": "pass123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/api/v1/auth/register", json={"email": "wrongpw@example.com", "password": "correctpass"})
    response = client.post("/api/v1/auth/login", data={"username": "wrongpw@example.com", "password": "wrongpass"})
    assert response.status_code == 401


def test_me(client):
    client.post("/api/v1/auth/register", json={"email": "me@example.com", "password": "pass123"})
    login = client.post("/api/v1/auth/login", data={"username": "me@example.com", "password": "pass123"})
    token = login.json()["access_token"]
    response = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"


def test_refresh_token(client):
    client.post("/api/v1/auth/register", json={"email": "refresh@example.com", "password": "pass123"})
    login = client.post("/api/v1/auth/login", data={"username": "refresh@example.com", "password": "pass123"})
    refresh_token = login.json()["refresh_token"]
    response = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_me_unauthorized(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
