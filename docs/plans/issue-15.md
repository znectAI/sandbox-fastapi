Status: ready

## Summary
Add a `GET /items/{item_id}/exists` endpoint to `app/main.py`. It reports whether an id is present in
the in-memory `ITEMS` store, always with status 200 for valid integer ids, so clients can check for an
item without handling a 404.

## Interfaces
- Endpoint: `GET /items/{item_id}/exists`
  - Path param `item_id: int`. FastAPI validates it; a non-integer (e.g. `/items/abc/exists`)
    returns 422 with FastAPI's default validation error body (`{"detail": [...]}`).
  - 200 OK, body `{"exists": true}` when `item_id` is a key in `ITEMS`.
  - 200 OK, body `{"exists": false}` when it is not. This route never returns 404.
  - `exists` is always a JSON boolean, never a string or an int.
- Python handler in `app/main.py`:
  `def item_exists(item_id: int) -> dict:` returns `{"exists": item_id in ITEMS}`.

## Files to change
- `app/main.py`: add the `item_exists` route after the existing item routes. Return
  `{"exists": item_id in ITEMS}`. Look up `ITEMS` at request time (module global) so tests can
  monkeypatch `app.main.ITEMS`. Do not change `ITEMS` or the existing routes.
- `tests/test_main.py`: add the tests listed below.

## Acceptance criteria
1. `GET /items/1/exists` returns status 200 and exactly `{"exists": true}`.
2. `GET /items/999/exists` returns status 200 and exactly `{"exists": false}`.
3. `GET /items/abc/exists` (a non-integer id) returns status 422.
4. The full pytest suite passes, including the existing tests.

## Test plan
- AC1: `test_item_exists_true`: `client.get("/items/1/exists")`. Assert `status_code == 200` and
  `json() == {"exists": True}`. Also assert `json()["exists"] is True` (a boolean, not truthy).
- AC2: `test_item_exists_false`: `client.get("/items/999/exists")`. Assert `status_code == 200`
  and `json() == {"exists": False}`, and `json()["exists"] is False`.
- AC3: `test_item_exists_non_integer_returns_422`: `client.get("/items/abc/exists")`. Assert
  `status_code == 422`. Optionally also check `/items/1.5/exists` returns 422.
- Extra (store is read live): `test_item_exists_uses_current_items(monkeypatch)`: set
  `app.main.ITEMS` to `{}` and assert `/items/1/exists` returns `{"exists": False}`.
- AC4: run `pytest`; every test passes.

## Risks and assumptions
- Assumes "exists" means "the id is a key in `ITEMS`". There is no deletion or soft-delete concept,
  so nothing else needs to be considered.
- Assumes the 422 body is FastAPI's default. The story only specifies the status code, so tests
  should assert the status only.
- Negative ids and 0 are valid ints, so they return `{"exists": false}` with 200. Not tested, as the
  story does not mention them.
- No route conflict: `/items/{item_id}/exists` has an extra path segment, like `/items/{item_id}/name`.
- No new dependencies are needed.
