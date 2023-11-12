from typing import Union, Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: str
    balances: Dict[str, int] = {}

class Order(BaseModel):
    userId: str
    price: float
    quantity: int

class OrderItem(BaseModel):
    side: str
    order: Order


TICKER = "GOOGLE"

users: List[User] = [
    {
        "id": "1",
        "balances": {
            "GOOGLE": 10,
            "USD": 50000,
        }
    },
    {
        "id": "2",
        "balances": {
            "GOOGLE": 10,
            "USD": 50000,
        }
    }
]

bids: List[Order] = []
asks: List[Order] = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/order/")
def place_order(orderItem: Dict):
    side = orderItem["side"]
    price = orderItem["price"]
    quantity = orderItem["quantity"]
    userId = orderItem["userId"]
    remainingQty = fillOrders(side, price, quantity, userId)

    if (remainingQty == 0):
        return {"filledQuantity": quantity}
    
    if (side == "bid"):
        bids.append({
            "userId": userId,
            "price": price,
            "quantity": quantity,
        })
        bids.sort(key=lambda x : x["price"])

    else:
        asks.append({
            "userId": userId,
            "price": price,
            "quantity": quantity,
        })
        asks.sort(key=lambda x: x["price"], reverse=True)

    return {"filledQuantity": quantity - remainingQty}


@app.get("/depth")
def get_depth():
    depth = {}
    for i in range(len(bids)):
        if bids[i]["price"] not in depth:
            depth[bids[i]["price"]] = {
                "quantity": bids[i]["quantity"],
                "type": "bid",
            }
        else:
            depth[bids[i]["price"]]["quantity"] += bids[i]["quantity"]

    for i in range(len(asks)):
        if asks[i]["price"] not in depth:
            depth[asks[i]["price"]] = {
                "quantity": asks[i]["quantity"],
                "type": "ask",
            }
        else:
            depth[asks[i]["price"]]["quantity"] += asks[i]["quantity"]

    return depth


@app.get("/balance/{userId}")
def get_user_balance(userId: str):
    user = [u for u in users if u["id"] == userId]

    if user:
        return {"balances": user[0]["balances"]}
    
    else:
        return {"USD": 0, TICKER: 0}
    

@app.get("/quote")
def get_quote():
    return {"message": "assignment"}


def flipBalance(userId1: str, userId2: str, quantity: int, price: float):
    user1 = [u for u in users if u["id"] == userId1]
    user2 = [u for u in users if u["id"] == userId2]
    if user1 and user2:
        user1[0]["balances"][TICKER] -= quantity
        user2[0]["balances"][TICKER] += quantity
        user1[0]["balances"]["USD"] += (quantity * price)
        user2[0]["balances"]["USD"] -= (quantity * price)


def fillOrders(side: str, price: float, quantity: int, userId: str):
    remainingQty = quantity

    if side == "bid":
        for i in range(len(asks)-1, -1, -1):
            if price < asks[i]["price"]:
                continue

            if asks[i]["quantity"] > remainingQty:
                asks[i]["quantity"] -= remainingQty
                flipBalance(asks[i]["userId"], userId, remainingQty, asks[i]["price"])
                return 0
            else:
                remainingQty -= asks[i]["quantity"]
                flipBalance(asks[i]["userId"], userId, asks[i]["quantity"], asks[i]["price"])
                asks.pop()

    else:
        for i in range(len(bids)-1, -1, -1):
            if price > bids[i]["price"]:
                continue

            if bids[i]["quantity"] > remainingQty:
                bids[i]["quantity"] -= remainingQty
                flipBalance(userId, bids[i]["userId"], remainingQty, bids[i]["price"])
                return 0
            else:
                remainingQty -= bids[i]["quantity"]
                flipBalance(userId, bids[i]["userId"], bids[i]["quantity"], bids[i]["price"])
                bids.pop()

    return remainingQty