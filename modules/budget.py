import os
import sqlite3

from modules.clear import clear


BUDGETS_DB_PATH = os.path.join("databases", "budgets.db")
user_id = None
recent_budgets = []


def display_recent_budget():
    global recent_budgets

    conn = sqlite3.connect(BUDGETS_DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM budgets WHERE user_id = ? ORDER BY id DESC LIMIT 5",
        (user_id,),
    )
    recent_budgets = c.fetchall()
    conn.close()

    print("Recent Budgets Created:")

    # id INTEGER PRIMARY KEY,
    # category TEXT,
    # amount REAL,
    # date DATE,
    # user_id INTEGER

    if recent_budgets == []:
        print("*No recent budgets")
    else:
        print("# \t Category \t\t\t Amount \t Date")
        for index, data in enumerate(recent_budgets):
            if len(data[1]) < 6:
                print(
                    f"{index+1} \t {data[1]} \t\t\t {data[2]} \t\t {str(data[3])[:7]}"
                )
            else:
                print(f"{index+1} \t {data[1]} \t\t {data[2]} \t\t {str(data[3])[:7]}")


def add_budget():
    clear()

    while True:
        print(
            """
What monthly budget category would you want to enter?
1 - Housing expense
2 - Tranportation expense
3 - Food expense
4 - Other expenses
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
            case _:
                clear()
                print("Enter a valid category number!")

    amount = input("Enter budget amount in USD: ")
    month = input("Enter month of this budget (Ex: 02): ")
    year = input("Enter year of this budget (Ex: 2024): ")
    date = f"{year}-{month}-{1}"

    conn = sqlite3.connect(BUDGETS_DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO budgets (category, amount, date, user_id)
        VALUES (?, ?, ?, ?)
    """,
        (category, amount, date, user_id),
    )

    conn.commit()
    conn.close()

    clear()
    print("Budget successfully added!")


def edit_budget():
    global recent_budgets
    while True:
        display_recent_budget()
        print("What transaction you wanted to edit?")
        selection = input("Enter number from 1 to 4: ")
        clear()

        if 0 < int(selection) <= len(recent_budgets):
            edit_item(selection)
            print("Successfully edited the budget!")
            break
        else:
            print("Transaction does not exist! Please try again.")


def edit_item(selection):
    global recent_budgets
    item_id = recent_budgets[int(selection) - 1][0]

    conn = sqlite3.connect(BUDGETS_DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM budgets WHERE id = ?",
        (item_id,),
    )
    budget_to_edit = c.fetchone()
    conn.close()

    print("Budget to edit:")

    print("Category \t\t\t Amount \t Date")

    if len(budget_to_edit[1]) < 6:
        print(
            f"{budget_to_edit[1]} \t\t\t {budget_to_edit[2]} \t\t {str(budget_to_edit[3])[:7]}"
        )
    else:
        print(
            f"{budget_to_edit[1]} \t\t {budget_to_edit[2]} \t\t {str(budget_to_edit[3])[:7]}"
        )

    while True:
        print(
            """
What category does this budget fall?
1 - Housing expense
2 - Tranportation expense
3 - Food expense
4 - Other expenses
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
            case _:
                clear()
                print("Enter a valid category number!")

    amount = input("Re-enter budget amount in USD: ")
    month = input("Re-enter the budget month (Ex: 02): ")
    year = input("Re-enter the budget year (Ex: 2024): ")
    date = f"{year}-{month}-{1}"
    conn = sqlite3.connect(BUDGETS_DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        UPDATE budgets
        SET amount = ?, date = ?, category = ?
        WHERE id = ?
        """,
        (amount, date, category, item_id),
    )

    conn.commit()
    conn.close()
    clear()


def delete_budget():
    global recent_budgets
    while True:
        display_recent_budget()
        print("What budget you wanted to delete?")
        selection = input("Enter number from 1 to 5: ")

        if 0 < int(selection) <= len(recent_budgets):
            confirm = input("Are you sure to delete? (Enter either Y or N): ")
            if confirm == "Y" or confirm == "y":
                item_id = recent_budgets[int(selection) - 1][0]

                conn = sqlite3.connect(BUDGETS_DB_PATH)
                c = conn.cursor()
                c.execute(
                    """
                    DELETE FROM budgets
                    WHERE id = ?
                    """,
                    (item_id,),
                )
                conn.commit()
                conn.close()

                clear()
                print("Successfully deleted the budget!")
                break
        else:
            print("Budget does not exist! Please try again.")


def budget(user_id_passed):
    global user_id
    user_id = user_id_passed
    while True:
        display_recent_budget()

        print(
            """
What would you want to do today?
            
1 - Add a new budget
2 - Edit recent budget entry
3 - Delete a recent budget
4 - Go back to menu
        """
        )

        match input("Your selection: "):
            case "1":
                add_budget()
            case "2":
                clear()
                edit_budget()
            case "3":
                clear()
                delete_budget()
            case "4":
                clear()
                return None
            case _:
                print("Enter a valid number!")
