import sqlite3
import os

from modules.clear import clear

TRANSACTIONS_DB_PATH = os.path.join("databases", "transactions.db")
BUDGETS_DB_PATH = os.path.join("databases", "budgets.db")
user_id = None


def comparison():
    month = ""
    year = ""

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
                month = ""
                break
            case "3":
                clear()
                return None
            case _:
                print("Enter a valid number!")

    generate_comparison(year, month)


def generate_comparison(year, month):
    categories = ["Housing", "Transportation", "Food", "Others"]

    # Retrieving and Creating the Transactions Dictionary

    conn = sqlite3.connect(TRANSACTIONS_DB_PATH)
    c = conn.cursor()
    if month == "":
        c.execute(
            """
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
            (year, user_id),
        )
    else:
        c.execute(
            """
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
            (year, month, user_id),
        )
    transactions = c.fetchall()
    conn.close()

    transactions_total = 0
    for transaction in transactions:
        transactions_total += transaction[1]
    transactions_dict = {row[0]: row[1] for row in transactions}
    if "Income" in transactions_dict:
        transactions_dict["Total"] = transactions_total - transactions_dict["Income"]
    else:
        transactions_dict["Total"] = transactions_total
        transactions_dict['Income'] = 0

    for category in categories:
        if category not in transactions_dict:
            transactions_dict[category] = 0

    # Retreiving and Creating the budget dictionary

    conn = sqlite3.connect(BUDGETS_DB_PATH)
    c = conn.cursor()
    if month == "":
        c.execute(
            """
            SELECT
                category,
                SUM(amount) AS total
            FROM
                budgets
            WHERE
                strftime('%Y', date) = ? AND user_id = ?
            GROUP BY
                category
            """,
            (year, user_id),
        )
    else:
        c.execute(
            """
            SELECT
                category,
                SUM(amount) AS total
            FROM
                budgets
            WHERE
                strftime('%Y', date) = ? AND strftime('%m', date) = ? AND user_id = ?
            GROUP BY
                category
            """,
            (year, month, user_id),
        )
    budgets = c.fetchall()
    conn.close()

    budget_total = 0
    for budget in budgets:
        budget_total += budget[1]
    budgets_dict = {row[0]: row[1] for row in budgets}
    budgets_dict["Total"] = budget_total

    for category in categories:
        if category not in budgets_dict:
            budgets_dict[category] = 0

    print("Category \t Income \t Expense \t Budget")

    for category in categories:
        print(
            f"{category} \t N/A \t\t {transactions_dict[category]} \t\t {budgets_dict[category]}"
        )
        if category == "Others":
            print(
                f"Total \t\t {transactions_dict['Income']} \t\t {transactions_dict['Total']} \t\t {budgets_dict['Total']}"
            )
    input('\n Press any key to exit the report.. ')
    clear()


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
