from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    assert client.get('/health').json() == {'status': 'ok'}


def test_products():
    response = client.get('/products')
    assert response.status_code == 200
    assert len(response.json()) >= 3


def test_checkout_requires_confirmation():
    user = 'confirmation-test'
    response = client.post(f'/cart/{user}/items', json={'product_id': 1, 'quantity': 1})
    assert response.status_code == 200
    response = client.post('/checkout', json={'user_id': user, 'confirm': False})
    assert response.status_code == 403


def test_checkout_success():
    user = 'checkout-test'
    assert client.post(f'/cart/{user}/items', json={'product_id': 2, 'quantity': 1}).status_code == 200
    response = client.post('/checkout', json={'user_id': user, 'confirm': True})
    assert response.status_code == 200
    order = response.json()
    assert order['status'] == 'placed'
    assert client.get(f"/orders/{order['order_id']}").status_code == 200


def test_insufficient_inventory():
    response = client.post('/cart/inventory-test/items', json={'product_id': 3, 'quantity': 99})
    assert response.status_code == 409


def test_assistant_requires_key(monkeypatch):
    monkeypatch.delenv('ANTHROPIC_API_KEY', raising=False)
    assert client.post('/assistant', json={'message': 'Hello'}).status_code == 503
