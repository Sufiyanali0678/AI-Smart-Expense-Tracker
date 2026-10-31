
from flask import Flask, render_template, request, redirect
import sqlite3
from model import predict_category

app = Flask(__name__)

# Database setup
def create_database():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            category TEXT DEFAULT 'Uncategorized'
        )
    """)

    # Add category column to an older database if needed
    cursor.execute("PRAGMA table_info(expenses)")
    columns = [column[1] for column in cursor.fetchall()]

    if "category" not in columns:
        cursor.execute("""
            ALTER TABLE expenses
            ADD COLUMN category TEXT DEFAULT 'Uncategorized'
        """)

    conn.commit()
    conn.close()


# Homepage
@app.route("/")
def home():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses ORDER BY id DESC")
    expenses = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total
    )


# Add expense with AI prediction
@app.route("/add", methods=["POST"])
def add_expense():
    description = request.form["description"].strip()
    amount = float(request.form["amount"])

    if description and amount > 0:
        category = predict_category(description)

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO expenses
            (description, amount, category)
            VALUES (?, ?, ?)""",
            (description, amount, category)
        )

        conn.commit()
        conn.close()

    return redirect("/")


create_database()

if __name__ == "__main__":
    app.run(debug=True)
