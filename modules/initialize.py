import os
import sqlite3

USERS_DB_PATH = os.path.join("databases", "users.db")
TRANSACTIONS_DB_PATH = os.path.join("databases", "transactions.db")
BUDGETS_DB_PATH = os.path.join("databases", "budgets.db")
INVESTMENTS_DB_PATH = os.path.join("databases", "investments.db")


def create_users_db():
    conn = sqlite3.connect(USERS_DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def create_transactions_db():
    conn = sqlite3.connect(TRANSACTIONS_DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            item TEXT,
            amount REAL,
            date DATE,
            category TEXT,
            user_id INTEGER
        )
    """
    )
    conn.commit()
    conn.close()


def create_budgets_db():
    conn = sqlite3.connect(BUDGETS_DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY,
            category TEXT,
            amount REAL,
            date DATE,
            user_id INTEGER
        )
    """
    )
    conn.commit()
    conn.close()


def create_investments_db():
    conn = sqlite3.connect(INVESTMENTS_DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS investments (
            id INTEGER PRIMARY KEY,
            item TEXT,
            year_invested INTEGER,
            principal REAL,
            interest REAL,
            year_maturity INTEGER,
            future_value REAL,
            user_id INTEGER
        )
    """
    )
    conn.commit()
    conn.close()


def initialize():
    if not os.path.exists("databases"):
        os.makedirs("databases")

    create_users_db()
    create_transactions_db()
    create_budgets_db()
    create_investments_db()
