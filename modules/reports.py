import sqlite3
import os

from modules.clear import clear

TRANSACTIONS_DB_PATH = os.path.join("databases", "transactions.db")
user_id = None


def comparison():
    month = ''
    year = ''

    while True:
        print(
            """Are you looking for a monthly or yearly view?

1 - Monthly view
2 - Yearly view
3 - Go back to menu
        """
        )
        action = input("Your selection: ")
        clear()
        match action:
            case "1":
                year = input("What year you want to view? (Ex: 2024): ")
                month = input(
                    "Which month of the year you want to view? (Ex: 08 for August): "
                )
                break
            case "2":
                year = input("What year you want to view? (Ex: 2024): ")
                month = ''
                break
            case "3":
                clear()
                return None
            case _:
                print("Enter a valid number!")

    generate_comparison(year, month)


def generate_comparison(year, month):
    conn = sqlite3.connect(TRANSACTIONS_DB_PATH)
    c = conn.cursor()

    if month == '':
        c.execute("""
            SELECT
                category,
                SUM(amount) AS total
            FROM
                transactions
            WHERE
                strftime('%Y', date) = ? AND user_id = ?
            GROUP BY
                category
            """,
            (year, user_id,)
        )
    else:
        c.execute("""
            SELECT
                category,
                SUM(amount) AS total
            FROM
                transactions
            WHERE
                strftime('%Y', date) = ? AND strftime('%m', date) = ? AND user_id = ?
            GROUP BY
                category
            """,
            (year, month, user_id)
        )

    transactions = c.fetchall()
    conn.close()

    transactions_dict = {row[0]: row[1] for row in transactions}

    # Next is to do the same for budget, then layout the table

def reports(user_id_passed):
    global user_id
    user_id = user_id_passed

    while True:
        print(
            """Which report you'd like to generate today?

1 - Compare Total Income & Expense against Total Budget
2 - View Investment Maturity
3 - Go back to menu
        """
        )
        action = input("Your selection: ")
        clear()
        match action:
            case "1":
                comparison()
            case "2":
                print("view investment maturity module goes here")
            case "3":
                clear()
                return None
            case _:
                print("Enter a valid number!")
