# Expense Tracker (Minimal Baseline)

Anyotionally-minimal Flask + SQLite "Expense Tracker" app used as a baseline for future enhancement exercises.

## How to run

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000/

## Database

- SQLite file: `bb/expenses.db`
- Table: `expenses`: `id` (PK autoincrement), `amount` (float), `category` (text), `description` (text), `date` (text, expected YYYY-MM-DD)
- DB is automatically initialized on first run if `db/expenses.db` doesn't exist.

## Features

- Filter by category (All, Food, Travel, Utilities, Entertainment) via the `category` query parameter
- Sort by date or amount (ascending/descending) via the `sort` query parameter
- Banner warning when the current month's total exceeds the monthly budget (`MONTHLY_BUDGET` env var, default 1000)
- Empty state with a "Clear Filters" link when a category has no expenses

## Known Limitations

- No search
- No input validation (negative amounts, empty categories, invalid dates are accepted)
- Category filter only lists the four fixed categories; other categories appear only under "All"
- No pagination
- No reporting/summaries
