# Issue #13: changes made

Companion to `docs/plans/issue-13.md`. It records what was implemented. The plan itself is unchanged.

## Implemented (matches the plan)
- `app/main.py`: added `list_items()` at `@app.get("/items")`. It returns
  `[{"id": item["id"], "name": item["name"]} for item in ITEMS.values()]`, in insertion order.
- `tests/test_main.py`: added `test_list_items` (AC1, AC2) and `test_list_items_empty` (AC3).
- `ITEMS` and the existing routes are unchanged.

## Intermediate work reverted during review iteration
- A commit sorted `GET /items` by name and changed the 404 detail to "not found". Both were reverted
  because the plan specifies insertion order and does not change the 404 detail ("Item not found").
  The final code has neither change.

## Verification
- `ruff check .` and `pytest -q --cov=app --cov-report=term-missing --cov-fail-under=80` both pass.
