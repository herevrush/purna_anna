def test_checkout_empty_cart(client, user_token):
    response = client.post("/api/v1/orders/", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 400


def test_checkout_success(client, admin_token, user_token):
    product = client.post(
        "/api/v1/products/",
        json={"name": "Grape", "slug": "grape", "price": "5.00", "stock_quantity": 100},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    product_id = product.json()["id"]
    client.post(
        "/api/v1/cart/items",
        json={"product_id": product_id, "quantity": 3},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    response = client.post("/api/v1/orders/", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert len(data["items"]) == 1
    assert float(data["total"]) == 15.0


def test_list_orders(client, user_token):
    response = client.get("/api/v1/orders/", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_order(client, admin_token, user_token):
    product = client.post(
        "/api/v1/products/",
        json={"name": "Strawberry", "slug": "strawberry", "price": "6.00", "stock_quantity": 50},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    product_id = product.json()["id"]
    client.post(
        "/api/v1/cart/items",
        json={"product_id": product_id, "quantity": 1},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    checkout = client.post("/api/v1/orders/", headers={"Authorization": f"Bearer {user_token}"})
    order_id = checkout.json()["id"]
    response = client.get(f"/api/v1/orders/{order_id}", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json()["id"] == order_id
