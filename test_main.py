from fastapi.testclient import TestClient
from main import app, TICKER

client = TestClient(app)

def test_read_main():
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {"Hello": "World"}

def test_initial_user_balances():
  response = client.get("/balance/1")
  assert response.status_code == 200
  assert response.json()["balances"][TICKER] == 10
  response = client.get("/balance/2")
  assert response.status_code == 200
  assert response.json()["balances"][TICKER] == 10


def test_initial_user_balances():
  response = client.get("/balance/1")
  assert response.status_code == 200
  assert response.json()["balances"][TICKER] == 10
  response = client.get("/balance/2")
  assert response.status_code == 200
  assert response.json()["balances"][TICKER] == 10


def test_orders_endpoint():
  response = client.post(
      "/order/",
      json={
          "type": "limit",
          "side": "bid",
          "price": 1400.1,
          "quantity": 1,
          "userId": "1"
      },
  )
  assert response.status_code == 200
  assert response.json()["filledQuantity"] == 0

  response = client.post(
      "/order/",
      json={
          "type": "limit",
          "side": "ask",
          "price": 1400.9,
          "quantity": 10,
          "userId": "2"
      },
  )
  assert response.status_code == 200
  assert response.json()["filledQuantity"] == 0

  response = client.post(
      "/order/",
      json={
          "type": "limit",
          "side": "ask",
          "price": 1501,
          "quantity": 5,
          "userId": "2"
      },
  )
  assert response.status_code == 200
  assert response.json()["filledQuantity"] == 0

  response = client.get("/depth")
  assert response.status_code == 200
  assert response.json()["1501"]["quantity"] == 5


def test_filled_order():
  response = client.post(
      "/order/",
      json={
          "type": "limit",
          "side": "bid",
          "price": 1502,
          "quantity": 2,
          "userId": "1"
      },
  )
  assert response.status_code == 200
  assert response.json()["filledQuantity"] == 2


def test_depth_update():
  response = client.get("/depth")
  assert response.status_code == 200
  assert response.json()["1400.9"]["quantity"] == 8

def test_balances_update():
  response = client.get("/balance/1")
  assert response.status_code == 200
  assert response.json()["balances"][TICKER] == 12
  assert response.json()["balances"]["USD"] == (50000 - 2 * 1400.9)
  response = client.get("/balance/2")
  assert response.status_code == 200
  assert response.json()["balances"][TICKER] == 8
  assert response.json()["balances"]["USD"] == (50000 + 2 * 1400.9)