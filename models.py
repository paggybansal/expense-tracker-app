import os
import sqlite3


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
    "amount_desc": "amount DESC",
    "amount_asc": "amount ASC",
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


def add_expense(amount, category, description, date):
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
    """Sum of amounts for dates starting with month_prefix (YYYY-MM)."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date LIKE ?",
        (month_prefix + "-%",),
    )
    total = cur.fetchone()[0]
    conn.close()
    return total
