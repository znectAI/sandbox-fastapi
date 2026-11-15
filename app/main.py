
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


@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = ITEMS.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
