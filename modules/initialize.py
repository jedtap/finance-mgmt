import os
import sqlite3

USERS_DB_PATH = os.path.join("databases", "users.db")


def create_db():
    if not os.path.exists("databases"):
        os.makedirs("databases")

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


def initialize():
    create_db()
