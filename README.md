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

## Known Limitations

This is intentionally limited functionality (baseline).

- No search
- No filtering
- No input validation (negative amounts, empty categories, invalid dates are accepted)
- No sorting
- No pagination
- No reporting/summaries
