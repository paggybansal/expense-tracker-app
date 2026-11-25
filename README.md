# Expense Tracker (Minimal Baseline)

Intentionally-minimal Flask + SQLite "Expense Tracker" app used as a baseline for future enhancement exercises.

## How to run

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000/

Start the app from the repository root: the database path `db/expenses.db` is relative to the working directory.

`python app.py` runs the Flask development server with debug on. For a production-style local run, use a WSGI server such as waitress (not listed in `requirements.txt`; install it separately):

```bash
pip install waitress
waitress-serve --listen=127.0.0.1:5000 app:app
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `MONTHLY_BUDGET` | `1000` | Monthly spending limit. A non-numeric or empty value logs a warning and falls back to 1000. |

Example: `MONTHLY_BUDGET=500 python app.py` (PowerShell: `$env:MONTHLY_BUDGET=500; python app.py`).

## Database

- SQLite file: `db/expenses.db`
- Table: `expenses`: `id` (PK autoincrement), `amount` (float), `category` (text), `description` (text), `date` (text, expected YYYY-MM-DD)
- DB is automatically initialized on first run if `db/expenses.db` doesn't exist.

## Features

### Category filter
A dropdown (All, Food, Travel, Utilities, Entertainment) driven by the `category` query parameter, e.g. `/?category=Food`. Unknown values fall back to All. Categories are hardcoded, so expenses in any other category appear only under All.

### Sorting
The `sort` query parameter accepts:

| Value | Order |
|-------|-------|
| `date_desc` (default) | Newest to oldest (ties broken by id, descending) |
| `date_asc` | Oldest to newest (ties broken by id, ascending) |
| `amount_desc` | High to low (ties broken by id, descending) |
| `amount_asc` | Low to high (ties broken by id, ascending) |

Unknown values fall back to `date_desc`. Filter and sort can be combined, e.g. `/?category=Food&sort=amount_desc`.

### Monthly budget banner
"⚠️ Warning: Monthly Budget Exceeded!" is shown when the current month's total (using the server's local date) is strictly greater than `MONTHLY_BUDGET`. The banner ignores the active category filter, so the total covers all categories.

### Empty state
When a category filter returns no rows, the page shows "No expenses found for this category" with a "Clear Filters" link. It is not shown for an empty database under All.

### Date handling
Dates should be entered as `YYYY-MM-DD`. `YYYY/MM/DD` and `MM/DD/YYYY` are normalized to `YYYY-MM-DD` when an expense is added and when the month total is computed. Other formats are stored as-is and are not counted in the month total.

## Known Limitations

- No search
- No pagination
- No input validation (negative amounts and empty categories are accepted)
- Hardcoded categories; expenses in other categories show only under "All"
- No message for an empty database under "All"
- No automated tests or CI
