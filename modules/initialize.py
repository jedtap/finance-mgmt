import os
import sqlite3

USERS_DB_PATH = os.path.join("databases", "users.db")
TRANSACTIONS_DB_PATH = os.path.join("databases", "transactions.db")

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
            user_id INTEGER,
            type TEXT
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
