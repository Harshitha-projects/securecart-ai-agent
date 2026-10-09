"""SecureCart AI demo API. In-memory data; not production authentication."""
import os
from collections import defaultdict
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="SecureCart AI", version="0.1.0")

PRODUCTS = {
    1: {"id": 1, "name": "Wireless Mouse", "price": 25.0, "stock": 10},
    2: {"id": 2, "name": "Mechanical Keyboard", "price": 85.0, "stock": 5},
    3: {"id": 3, "name": "USB-C Hub", "price": 40.0, "stock": 8},
}
CARTS: dict[str, dict[int, int]] = defaultdict(dict)
ORDERS: dict[str, dict] = {}


class CartItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, le=100)


class CheckoutRequest(BaseModel):
    user_id: str = Field(min_length=1)
    confirm: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/products")
def products():
    return list(PRODUCTS.values())


@app.get("/products/{product_id}")
def product(product_id: int):
    if product_id not in PRODUCTS:
        raise HTTPException(404, "Product not found")
    return PRODUCTS[product_id]


@app.post("/cart/{user_id}/items")
def add_item(user_id: str, item: CartItem):
    product_data = PRODUCTS.get(item.product_id)
    if product_data is None:
        raise HTTPException(404, "Product not found")
    updated = CARTS[user_id].get(item.product_id, 0) + item.quantity
    if updated > product_data["stock"]:
        raise HTTPException(409, "Insufficient inventory")
    CARTS[user_id][item.product_id] = updated
    return get_cart(user_id)


@app.get("/cart/{user_id}")
def get_cart(user_id: str):
    items = [
        {"product_id": pid, "name": PRODUCTS[pid]["name"], "quantity": qty,
         "unit_price": PRODUCTS[pid]["price"], "subtotal": round(qty * PRODUCTS[pid]["price"], 2)}
        for pid, qty in CARTS[user_id].items()
    ]
    return {"user_id": user_id, "items": items,
            "total": round(sum(item["subtotal"] for item in items), 2)}


@app.post("/checkout")
def checkout(request: CheckoutRequest):
    if not request.confirm:
        raise HTTPException(403, "Explicit checkout confirmation required")
    cart = get_cart(request.user_id)
    if not cart["items"]:
        raise HTTPException(400, "Cart is empty")
    for item in cart["items"]:
        if PRODUCTS[item["product_id"]]["stock"] < item["quantity"]:
            raise HTTPException(409, "Insufficient inventory")
    for item in cart["items"]:
        PRODUCTS[item["product_id"]]["stock"] -= item["quantity"]
    order_id = str(uuid4())
    order = {"order_id": order_id, "user_id": request.user_id,
             "items": cart["items"], "total": cart["total"], "status": "placed"}
    ORDERS[order_id] = order
    CARTS[request.user_id].clear()
    return order


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in ORDERS:
        raise HTTPException(404, "Order not found")
    return ORDERS[order_id]


class AssistantRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


@app.post("/assistant")
async def assistant(request: AssistantRequest):
    """Optional Claude response; does not execute purchases or access customer data."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(503, "Set ANTHROPIC_API_KEY to enable Claude")
    try:
        from anthropic import AsyncAnthropic
        client = AsyncAnthropic(api_key=api_key)
        response = await client.messages.create(
            model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5"),
            max_tokens=400,
            system="You are a helpful shopping assistant. You cannot place orders or claim to have checked live inventory.",
            messages=[{"role": "user", "content": request.message}],
        )
        return {"reply": "".join(block.text for block in response.content if block.type == "text")}
    except Exception as exc:
        raise HTTPException(502, "Claude request failed; check API key and model settings") from exc
