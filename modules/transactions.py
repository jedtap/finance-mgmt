import sqlite3
import os

from modules.clear import clear

TRANSACTIONS_DB_PATH = os.path.join("databases", "transactions.db")
transactions = []
user_id = None


def display_recent_transactions():
    conn = sqlite3.connect(TRANSACTIONS_DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER BY id DESC LIMIT 5",
        (user_id,),
    )
    transactions = c.fetchall()
    conn.close()

    print("Recent Transactions:")

    if transactions == []:
        print("*No recent transactions")
    else:
        print("# \t Item \t\t\t Amount \t Date \t Category")
        for index, data in enumerate(transactions):
            if len(data[1]) < 6:
                print(
                    f"{index+1} \t {data[1]} \t\t\t {data[2]} \t\t {data[3]} \t {data[4]}"
                )
            else:
                print(
                    f"{index+1} \t {data[1]} \t\t {data[2]} \t\t {data[3]} \t {data[4]}"
                )


def add_transaction():
    clear()
    item = input("Enter name of item: ")
    amount = input("Enter amount in USD: ")
    year = input("Enter year the transaction was made (Ex: 2024): ")
    month = input("Enter month the transaction was made (Ex: 02): ")
    date = f"{year}-{month}-{1}"

    while True:
        print(
            """
What category does this fall?
1 - Housing expense
2 - Tranportation expense
3 - Food expense
4 - Other expenses
5 - Income source
        """
        )
        category_index = input("Enter category number: ")
        match category_index:
            case "1":
                category = "Housing"
                break
            case "2":
                category = "Transportation"
                break
            case "3":
                category = "Food"
                break
            case "4":
                category = "Others"
                break
            case "5":
                category = "Income"
            case _:
                clear()
                print("Enter a valid category number!")

    conn = sqlite3.connect(TRANSACTIONS_DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO transactions (item, amount, date, category, user_id)
        VALUES (?, ?, ?, ?, ?)
    """,
        (item, amount, date, category, user_id),
    )

    conn.commit()
    conn.close()

    clear()
    print("Transaction successfully added!")


def transactions(user_id_passed):
    global user_id
    user_id = user_id_passed
    while True:
        display_recent_transactions()

        print(
            """
What would you want to do today?
            
1 - Add a new transaction
2 - Edit recent transactions
3 - Delete a recent transaction
4 - Go back to menu
        """
        )

        match input("Your selection: "):
            case "1":
                add_transaction()
            case "2":
                print("case 2") # Next module
            case "3":
                print("case 3")
            case "4":
                clear()
                return None
            case _:
                print("Enter a valid number!")
