"""FastAPI demo app.

Covers:
- Basic routes
- Path/query parameters
- Pydantic request/response models
- Headers/cookies
- Dependencies
- Custom errors

Run:
    uvicorn main:app --reload

Docs:
    http://127.0.0.1:8000/docs
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Cookie, Depends, FastAPI, Header, HTTPException, Path, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI(title="FastAPI demo", version="1.0.0")


# -----------------------------
# Models
# -----------------------------

class ItemIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    tags: list[str] = []


class ItemOut(BaseModel):
    id: int
    name: str
    price: float
    tags: list[str]


# A tiny in-memory "DB"
_ITEMS: dict[int, ItemOut] = {}
_NEXT_ID = 1


# -----------------------------
# Dependencies
# -----------------------------

def get_request_id(x_request_id: Annotated[str | None, Header()] = None) -> str:
    # If the client didn't provide one, generate something simple.
    # (In real apps you’d use uuid4.)
    return x_request_id or "req-demo"


# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(
    item_id: Annotated[int, Path(ge=1)],
    details: Annotated[bool, Query()] = False,
):
    item = _ITEMS.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    # 'details' is just here to demonstrate query params.
    # We don't change the response, but you could.
    return item


@app.get("/search")
def search(
    q: Annotated[str, Query(min_length=1)],
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    # Very small demo search against item names.
    hits = [i for i in _ITEMS.values() if q.lower() in i.name.lower()]
    return {"query": q, "count": len(hits), "items": hits[:limit]}


@app.post(
    "/items",
    response_model=ItemOut,
    status_code=status.HTTP_201_CREATED,
)
def create_item(
    payload: ItemIn,
    response: Response,
    request_id: str = Depends(get_request_id),
    session: Annotated[str | None, Cookie()] = None,
):
    global _NEXT_ID

    if session is None:
        # Show cookies: we can set one on the response.
        response.set_cookie("session", "demo-session")

    item = ItemOut(id=_NEXT_ID, name=payload.name, price=payload.price, tags=payload.tags)
    _ITEMS[_NEXT_ID] = item
    _NEXT_ID += 1

    # Show headers: include request id in response
    response.headers["X-Request-Id"] = request_id

    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: Annotated[int, Path(ge=1)]):
    if item_id not in _ITEMS:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    del _ITEMS[item_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# -----------------------------
# Custom error example
# -----------------------------

class DemoError(Exception):
    pass


@app.exception_handler(DemoError)
def demo_error_handler(_request, _exc: DemoError):
    # Return a custom structure.
    return Response(
        content='{"error":"demo_error","message":"Something went wrong (demo)"}',
        media_type="application/json",
        status_code=400,
    )


@app.get("/boom")
def boom():
    raise DemoError()
