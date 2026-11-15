Status: ready

## Summary
Add a `GET /items/{item_id}/name` endpoint to `app/main.py`. It returns only the item's name from the
existing in-memory `ITEMS` store, and returns 404 for unknown ids, the same way `GET /items/{item_id}` does.

## Interfaces
- Endpoint: `GET /items/{item_id}/name`
  - Path param `item_id: int` (FastAPI validation; a non-integer returns 422, as the existing route does).
  - 200 OK, body: `{"name": <str>}`. Example: `GET /items/1/name` -> `{"name": "widget"}`.
  - 404 Not Found when `item_id` is not in `ITEMS`. Body: `{"detail": "Item not found"}`
    (the same message as `GET /items/{item_id}`).
- Python handler in `app/main.py`:
  `def get_item_name(item_id: int) -> dict:`

## Files to change
- `app/main.py`: add the `get_item_name` route. Look up `ITEMS.get(item_id)`; if it is `None`, raise
  `HTTPException(status_code=404, detail="Item not found")`; otherwise return `{"name": item["name"]}`.
  Do not change `ITEMS` or the existing routes.
- `tests/test_main.py`: add the tests listed below.

## Acceptance criteria
1. `GET /items/1/name` returns status 200 and the body `{"name": "widget"}` exactly.
2. `GET /items/{id}/name` for an id not in `ITEMS` (e.g. 999) returns status 404 with the body
   `{"detail": "Item not found"}`.
3. pytest tests cover criteria 1 and 2, and the whole suite passes.

## Test plan
- AC1: `test_get_item_name`: `client.get("/items/1/name")`. Assert `status_code == 200` and
  `json() == {"name": "widget"}`.
- AC2: `test_get_item_name_unknown_returns_404`: `client.get("/items/999/name")`. Assert
  `status_code == 404` and `json() == {"detail": "Item not found"}`.
- AC3: run `pytest` and confirm the new tests and the existing tests all pass.

## Risks and assumptions
- Assumes the 404 body should be the same as the existing item route's (`"Item not found"`); the story
  does not specify a body.
- Assumes non-integer ids return FastAPI's default 422. This is not tested because the story does not
  require it.
- No route conflict: `/items/{item_id}/name` has an extra path segment, so it does not overlap with
  `/items/{item_id}`.
- No new dependencies are needed.
