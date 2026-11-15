Status: ready

## Summary
Add a `GET /items` endpoint to `app/main.py` that returns every item in the existing in-memory `ITEMS`
store as a JSON list of `{"id", "name"}` objects.

## Interfaces
- Endpoint: `GET /items`
  - No path or query parameters.
  - 200 OK, body: a JSON array of objects, each exactly `{"id": <int>, "name": <str>}`, in `ITEMS`
    insertion order (ascending id for the current data).
    Example with current data: `GET /items` -> `[{"id": 1, "name": "widget"}]`.
  - If `ITEMS` is empty, returns 200 with `[]` (never 404).
  - No error cases.
- Python handler in `app/main.py`:
  `def list_items() -> list[dict]:`

## Files to change
- `app/main.py`: add the `list_items` route, decorated `@app.get("/items")`. Return
  `[{"id": item["id"], "name": item["name"]} for item in ITEMS.values()]`, so the output has only the
  `id` and `name` keys even if items gain more fields later. Do not change `ITEMS` or the existing routes.
- `tests/test_main.py`: add the tests listed below.

## Acceptance criteria
1. `GET /items` returns status 200 and a JSON list in which every element is an object with exactly the
   keys `id` and `name`.
2. With the current data, `GET /items` returns exactly `[{"id": 1, "name": "widget"}]`.
3. When `ITEMS` is empty, `GET /items` returns status 200 and `[]`.
4. pytest tests cover criteria 1 to 3, and the whole suite passes.

## Test plan
- AC1 + AC2: `test_list_items`: `client.get("/items")`. Assert `status_code == 200`, `json()` is a
  `list`, every element has `set(keys) == {"id", "name"}`, and `json() == [{"id": 1, "name": "widget"}]`.
- AC3: `test_list_items_empty`: use pytest's `monkeypatch.setattr("app.main.ITEMS", {})`, then
  `client.get("/items")`. Assert `status_code == 200` and `json() == []`. (Monkeypatch restores
  `ITEMS` after the test, so other tests are not affected.)
- AC4: run `pytest` and confirm the new tests and the existing tests all pass.

## Risks and assumptions
- Assumes the response is a bare JSON array, not an object that wraps the list (e.g. `{"items": [...]}`),
  because the story says "returns a list".
- Assumes no pagination, filtering or sorting is needed; the store is small and in memory.
- Assumes an empty store returns `[]` with status 200; the story does not say.
- No route conflict: `/items` has no path parameter, so it does not overlap with `/items/{item_id}`.
- No new dependencies are needed.
