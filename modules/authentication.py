import getpass
import hashlib
import os
import sqlite3

from modules.clear import clear

USERS_DB_PATH = os.path.join("databases", "users.db")


def welcome():
    while True:
        print(
            """
Welcome to the Personal Finance Tracker! Press any of the following to continue:

1 - Login
2 - Create an account
        """
        )
        action = input("Your selection: ")
        clear()
        if action == "1" or action == "2":
            break
        else:
            print("Invalid selection, please try again.")
    return action


def create_account():
    while True:
        username = input("Enter username (or Enter to go back to screen): ")
        if username == "":
            clear()
            break

        password = getpass.getpass("Enter password: ")
        verify_password = getpass.getpass("Verify password: ")
        clear()

        conn = sqlite3.connect(USERS_DB_PATH)
        c = conn.cursor()
        c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        username_exists = c.fetchone() is not None
        conn.close()

        if password != verify_password:
            print("Password is not the same.")
        elif username_exists:
            print("Username already exists! Please try another username.")
        else:
            hashed_password = hash_password(password)
            conn = sqlite3.connect(USERS_DB_PATH)
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password),
            )
            conn.commit()
            conn.close()
            input("Your account is created! Press enter to continue. ")
            clear()
            break


def hash_password(password):
    hasher = hashlib.sha256()
    hasher.update(password.encode("utf-8"))
    return hasher.hexdigest()


def login():
    while True:
        username = input("Enter username (or Enter to go back to screen): ")
        if username == "":
            clear()
            break

        password = getpass.getpass("Enter password: ")
        hashed_password = hash_password(password)
        clear()

        conn = sqlite3.connect(USERS_DB_PATH)
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        stored_password = c.fetchone()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_id = c.fetchone()
        conn.close()

        if stored_password and stored_password[0] == hashed_password:
            return user_id
        else:
            print("Username and/or password is incorrect. Please try again. ")


def authentication():
    action = 0
    while True:
        action = welcome()
        if action == "1":
            user_id = login()
            if user_id is not None:
                clear()
                print('Successfully logged in!')
                return user_id
        else:
            create_account()
