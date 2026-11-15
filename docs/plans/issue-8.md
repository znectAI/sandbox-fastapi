Status: ready

## Summary
Add a `GET /version` endpoint to the FastAPI app that returns the app version
(`{"version": "0.1.0"}`), backed by a single module-level constant, plus a pytest test.

## Interfaces
- Module constant in `app/main.py`:
  - `VERSION: str = "0.1.0"`
- Endpoint:
  - `GET /version`
  - Handler: `def version() -> dict` in `app/main.py`, registered with `@app.get("/version")`
  - Request: no parameters, no body.
  - Response: `200 OK`, `Content-Type: application/json`, body exactly `{"version": "0.1.0"}`
    (i.e. `{"version": VERSION}`).
  - Error cases: none specific to this endpoint. Other methods (e.g. `POST /version`)
    get FastAPI's default `405 Method Not Allowed`.

## Files to change
- `app/main.py`: add `VERSION = "0.1.0"` near the top (after `app = FastAPI()` or
  before it), and add the `/version` route following the style of `/health`.
- `tests/test_main.py`: add `test_version` (see Test plan).

No new packages; no changes to `pyproject.toml`, `requirements*.txt`, or `.github/*`.

## Acceptance criteria
1. `GET /version` responds with status 200 and JSON body `{"version": "0.1.0"}`. (Story AC1)
2. A pytest test in `tests/test_main.py` covers AC1 and passes with `pytest`. (Story AC2)
3. Existing tests (`/`, `/health`, `/items/{id}`) still pass.

## Test plan
- AC1 / AC2: `test_version` in `tests/test_main.py`, using the existing module-level
  `client = TestClient(app)`:
  ```python
  def test_version():
      response = client.get("/version")
      assert response.status_code == 200
      assert response.json() == {"version": "0.1.0"}
  ```
  Assert against the literal `"0.1.0"` (not `VERSION`) so the test pins the story's
  required value.
- AC3: run the full suite with `pytest`; all existing tests must still pass.

## Risks and assumptions
- Assumption: the version is a hard-coded constant. The repo has no packaging metadata
  (`pyproject.toml` only configures pytest; no `[project]` table), so reading it via
  `importlib.metadata` is not possible without adding packaging config, which is out of
  scope for the smallest change.
- Risk: the version string now lives in code; future releases must bump `VERSION` and the
  test's literal together. Acceptable for this story.
- Assumption: no authentication or extra fields (build hash, timestamp) are wanted; the
  response is exactly the one key.
