import uuid


def test_list_products(client):
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_product_not_found(client):
    response = client.get(f"/api/v1/products/{uuid.uuid4()}")
    assert response.status_code == 404


def test_create_product_requires_admin(client, user_token):
    response = client.post(
        "/api/v1/products/",
        json={"name": "Apple", "slug": "apple", "price": "1.99", "stock_quantity": 100},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 403


def test_create_product_as_admin(client, admin_token):
    response = client.post(
        "/api/v1/products/",
        json={"name": "Banana", "slug": "banana", "price": "0.99", "stock_quantity": 50},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Banana"
    assert data["slug"] == "banana"
    assert "id" in data


def test_create_and_get_product(client, admin_token):
    create = client.post(
        "/api/v1/products/",
        json={"name": "Carrot", "slug": "carrot", "price": "2.50", "stock_quantity": 30},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert create.status_code == 201
    product_id = create.json()["id"]
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Carrot"
