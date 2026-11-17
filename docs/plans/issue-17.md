Status: ready

## Summary
Add a `GET /ping` endpoint to `app/main.py` that always returns `{"pong": true}` with status 200,
giving clients a trivial liveness check.

## Interfaces
- Endpoint: `GET /ping`
  - No path or query parameters; any query string is ignored.
  - 200 OK, `Content-Type: application/json`, body exactly `{"pong": true}`.
  - `pong` is a JSON boolean `true`, not the string `"true"` and not `1`.
  - No error cases. Other methods (e.g. `POST /ping`) return FastAPI's default 405.
- Python handler in `app/main.py`:
  `def ping() -> dict:` returns `{"pong": True}`.

## Files to change
- `app/main.py`: add the `ping` route next to `/health` and `/version`. Do not change existing
  routes, `ITEMS` or `VERSION`.
- `tests/test_main.py`: add the tests listed below.

## Acceptance criteria
1. `GET /ping` returns status 200 and the JSON body exactly `{"pong": true}`.
2. The `pong` value is a JSON boolean `true`.
3. `POST /ping` returns status 405 (only GET is supported).
4. The full pytest suite passes, including the existing tests.

## Test plan
- AC1: `test_ac1_ping_returns_pong`: `client.get("/ping")`. Assert `status_code == 200` and
  `json() == {"pong": True}`.
- AC2: `test_ac2_ping_pong_is_boolean`: `client.get("/ping")`. Assert `json()["pong"] is True`.
- AC3: `test_ac3_ping_post_not_allowed`: `client.post("/ping")`. Assert `status_code == 405`.
- AC4: run `pytest`; every test passes.

## Risks and assumptions
- The story's curly quotes (`{“pong”: true}`) are read as ordinary JSON: key `"pong"`, boolean
  value `true`.
- Assumes `/ping` needs no auth and touches no state, like `/health`.
- AC3 tests FastAPI's default behaviour; the story only says "GET", so this is a light check.
- No route conflict: `/ping` is a new top-level path. No new dependencies.
