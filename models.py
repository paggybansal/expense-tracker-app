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


def get_all_expenses():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, amount, category, description, date FROM expenses")
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
