import csv
import io
import logging
import os
from datetime import date as _date

from flask import Flask, render_template, request, redirect, url_for, Response

from models import (
    init_db, get_all_expenses, add_expense, delete_expense, get_month_total, get_month_summary, SORT_OPTIONS,
)

app = Flask(__name__)

CATEGORIES = ["Food", "Travel", "Utilities", "Entertainment"]
SORT_LABELS = [
    ("date_desc", "Date: Newest to Oldest"),
    ("date_asc", "Date: Oldest to Newest"),
    ("amount_desc", "Amount: High to Low"),
    ("amount_asc", "Amount: Low to High"),
]
# Monthly budget limit; configurable via MONTHLY_BUDGET env var (default 1000)
DEFAULT_MONTHLY_BUDGET = 1000.0


def _parse_budget(raw):
    try:
        return float(raw)
    except (TypeError, ValueError):
        logging.warning("Invalid MONTHLY_BUDGET %r; using %s", raw, DEFAULT_MONTHLY_BUDGET)
        return DEFAULT_MONTHLY_BUDGET


MONTHLY_BUDGET = _parse_budget(os.environ.get("MONTHLY_BUDGET", DEFAULT_MONTHLY_BUDGET))

# Initialize DB (creates db/expenses.db on first run)
init_db()


def _filter_args():
    category = request.args.get("category", "All")
    if category != "All" and category not in CATEGORIES:
        category = "All"
    sort = request.args.get("sort", "date_desc")
    if sort not in SORT_OPTIONS:
        sort = "date_desc"
    return category, sort


def _csv_safe(value):
    # Neutralize spreadsheet formula injection
    text = "" if value is None else str(value)
    return "'" + text if text[:1] in ("=", "+", "-", "@") else text


@app.get("/export/csv")
def export_csv():
    category, sort = _filter_args()
    expenses = get_all_expenses(category, sort)
    if not expenses:
        return Response("No expense records available for export.", status=404, mimetype="text/plain")
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["ID", "Title", "Category", "Amount", "Date"])
    for e in expenses:
        writer.writerow([e["id"], _csv_safe(e["description"]), _csv_safe(e["category"]), e["amount"], e["date"]])
    return Response(
        buf.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=expenses.csv"},
    )


@app.get("/")
def index():
    category, sort = _filter_args()
    expenses = get_all_expenses(category, sort)
    today = _date.today()
    month_spent, top_category, avg_daily = get_month_summary(today.strftime("%Y-%m"), today)
    month_total = get_month_total(_date.today().strftime("%Y-%m"))
    return render_template(
        "index.html",
        expenses=expenses,
        categories=CATEGORIES,
        sort_labels=SORT_LABELS,
        selected_category=category,
        selected_sort=sort,
        month_spent=month_spent,
        top_category=top_category,
        avg_daily=avg_daily,
        budget_exceeded=month_total > MONTHLY_BUDGET,
    )


@app.get("/add")
def add_expense_form():
    return render_template("add_expense.html")


@app.post("/add")
def add_expense_post():
    amount = request.form.get("amount")
    category = request.form.get("category")
    description = request.form.get("description")
    date = request.form.get("date")

    add_expense(amount, category, description, date)
    return redirect(url_for("index"))


@app.post("/delete/<id>")
def delete(id):
    delete_expense(id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
