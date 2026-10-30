from flask import Flask, render_template, request, redirect, url_for

from models import init_db, get_all_expenses, add_expense, delete_expense

app = Flask(__name__)

# Initialize DB (creates db/expenses.db on first run)
init_db()


@app.get("/")
def index():
    expenses = get_all_expenses()
    return render_template("index.html", expenses=expenses)


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
