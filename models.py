import os
import sqlite3
from datetime import datetime


DB_PATH = os.path.join("db", "expenses.db")


def get_conn():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # Initialize database on first run if it doesn't exist
    if os.path.exists(DB_PATH):
        return

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        description TEXT,
        date TEXT
     );
    """)
    conn.commit()
    conn.close()


SORT_OPTIONS = {
    "date_desc": "date DESC, id DESC",
    "date_asc": "date ASC, id ASC",
    "amount_desc": "amount DESC, id DESC",
    "amount_asc": "amount ASC, id ASC",
}


def get_all_expenses(category=None, sort=None):
    order_by = SORT_OPTIONS.get(sort)  # whitelist only; never interpolate user input
    query = "SELECT id, amount, category, description, date FROM expenses"
    params = []
    if category and category != "All":
        query += " WHERE category = ?"
        params.append(category)
    if order_by:
        query += " ORDER BY " + order_by
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y")


def normalize_date(value):
    """Return value as YYYY-MM-DD if it matches a supported format, else unchanged."""
    text = (value or "").strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return value


def add_expense(amount, category, description, date):
    date = normalize_date(date)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
        (amount, category, description, date),
    )
    conn.commit()
    conn.close()


def delete_expense(expense_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()


def get_month_total(month_prefix):
    """Sum of amounts whose date falls in month_prefix (YYYY-MM).

    Dates in the supported formats are normalized first, so rows stored as
    YYYY/MM/DD or MM/DD/YYYY are counted too.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT amount, date FROM expenses")
    rows = cur.fetchall()
    conn.close()
    return sum(
        (row["amount"] or 0)
        for row in rows
        if str(normalize_date(row["date"])).startswith(month_prefix + "-")
    )


def get_month_summary(month_prefix, today):
    """Return (total, top_category, avg_daily) for month_prefix (YYYY-MM).

    avg_daily = total / elapsed days of the month (today.day). top_category is None if no spend.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT amount, category, date FROM expenses")
    rows = cur.fetchall()
    conn.close()
    total = 0.0
    by_cat = {}
    for row in rows:
        if str(normalize_date(row["date"])).startswith(month_prefix + "-"):
            amt = row["amount"] or 0
            total += amt
            cat = row["category"] or "Uncategorized"
            by_cat[cat] = by_cat.get(cat, 0) + amt
    top = max(by_cat, key=lambda c: (by_cat[c], c)) if by_cat else None
    return total, top, total / max(today.day, 1)
