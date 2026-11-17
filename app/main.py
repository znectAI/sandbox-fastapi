
from fastapi import FastAPI, HTTPException

app = FastAPI()

VERSION = "0.1.0"

ITEMS = {1: {"id": 1, "name": "widget"}}


@app.get("/")
def root():
    return {"message": "hello"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version() -> dict:
    return {"version": VERSION}


@app.get("/ping")
def ping() -> dict:
    return {"pong": True}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = ITEMS.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/items/{item_id}/name")
def get_item_name(item_id: int) -> dict:
    item = ITEMS.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": item["name"]}


@app.get("/items")
def list_items() -> list[dict]:
    return [{"id": item["id"], "name": item["name"]} for item in ITEMS.values()]


@app.get("/items/{item_id}/exists")
def item_exists(item_id: int) -> dict:
    return {"exists": item_id in ITEMS}
