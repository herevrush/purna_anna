def test_get_empty_cart(client, user_token):
    response = client.get("/api/v1/cart/", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json() == []


def test_add_to_cart(client, admin_token, user_token):
    product = client.post(
        "/api/v1/products/",
        json={"name": "Orange", "slug": "orange", "price": "1.50", "stock_quantity": 20},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    product_id = product.json()["id"]
    response = client.post(
        "/api/v1/cart/items",
        json={"product_id": product_id, "quantity": 2},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    assert response.json()["quantity"] == 2


def test_update_cart_item(client, admin_token, user_token):
    product = client.post(
        "/api/v1/products/",
        json={"name": "Mango", "slug": "mango", "price": "3.00", "stock_quantity": 15},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    product_id = product.json()["id"]
    item = client.post(
        "/api/v1/cart/items",
        json={"product_id": product_id, "quantity": 1},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    item_id = item.json()["id"]
    response = client.put(
        f"/api/v1/cart/items/{item_id}",
        json={"quantity": 5},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 5


def test_remove_from_cart(client, admin_token, user_token):
    product = client.post(
        "/api/v1/products/",
        json={"name": "Pineapple", "slug": "pineapple", "price": "4.00", "stock_quantity": 10},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    product_id = product.json()["id"]
    item = client.post(
        "/api/v1/cart/items",
        json={"product_id": product_id, "quantity": 1},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    item_id = item.json()["id"]
    response = client.delete(
        f"/api/v1/cart/items/{item_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 204
