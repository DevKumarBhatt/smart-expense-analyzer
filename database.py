
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "expenses.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_table():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        """)


def add_transaction(date, transaction_type, category, amount, description):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO transactions
            (date, transaction_type, category, amount, description)
            VALUES (?, ?, ?, ?, ?)
        """, (str(date), transaction_type, category, amount, description))


def get_transactions():
    with get_connection() as conn:
        return conn.execute("""
            SELECT date, transaction_type, category, amount, description
            FROM transactions
            ORDER BY date DESC, id DESC
        """).fetchall()

def create_budget_table():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month TEXT NOT NULL,
                category TEXT NOT NULL,
                budget_amount REAL NOT NULL,
                UNIQUE(month, category)
            )
        """)


def save_budget(month, category, budget_amount):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO budgets (month, category, budget_amount)
            VALUES (?, ?, ?)
            ON CONFLICT(month, category)
            DO UPDATE SET budget_amount = excluded.budget_amount
        """, (month, category, budget_amount))


def get_budgets(month):
    with get_connection() as conn:
        return conn.execute("""
            SELECT category, budget_amount
            FROM budgets
            WHERE month = ?
            ORDER BY category
        """, (month,)).fetchall()

    