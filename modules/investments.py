import sqlite3
import os

from modules.clear import clear

INVESTMENTS_DB_PATH = os.path.join("databases", "investments.db")
user_id = None
recent_investments = []


def display_recent_investments():
    global recent_investments

    conn = sqlite3.connect(INVESTMENTS_DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM investments WHERE user_id = ? ORDER BY id DESC LIMIT 5",
        (user_id,),
    )
    recent_investments = c.fetchall()
    conn.close()

    print("Recent Investments:")

    if recent_investments == []:
        print("*No recent investments")
    else:
        print("# \t Item \t\t Principal \t Interest \t Maturity Year \t Future Value")
        for index, data in enumerate(recent_investments):
            print(
                f"{index+1} \t {data[1]} \t {data[3]} \t {data[4]*100}% \t\t {data[5]} \t\t {int(data[6] * 100 + 0.9999)/100}"
            )


def add_investment():
    clear()
    item = input("Enter name of investment: ")
    year_invested = input("Enter start year of the investment: ")
    principal = float(input("Enter investment amount in USD: "))
    interest = float(input("Enter interest rate in percent: ")) / 100
    year_maturity = input("Enter maturity year of the investment: ")
    future_value = principal * pow(
        (1 + interest), (int(year_maturity) - int(year_invested))
    )

    conn = sqlite3.connect(INVESTMENTS_DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO investments (item, year_invested, principal, interest, year_maturity, future_value, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            item,
            year_invested,
            principal,
            interest,
            year_maturity,
            future_value,
            user_id,
        ),
    )

    conn.commit()
    conn.close()

    clear()
    print("Investment successfully added!")


def edit_investment():
    global recent_investments
    while True:
        display_recent_investments()
        print("What investment you wanted to edit?")
        selection = input("Enter number from 1 to 5: ")
        clear()

        if 0 < int(selection) <= len(recent_investments):
            edit_item(selection)
            print("Successfully edited the investment!")
            break
        else:
            print("Investment does not exist! Please try again.")


def edit_item(selection):
    global recent_investments
    item_id = recent_investments[int(selection) - 1][0]

    conn = sqlite3.connect(INVESTMENTS_DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM investments WHERE id = ?",
        (item_id,),
    )
    investment_to_edit = c.fetchone()
    conn.close()

    print("Investment to edit:")

    print(
        "Item \t\t\t Year Invested \t Principal \t Interest \t Maturity Year \t Future Value"
    )

    print(
        f"{investment_to_edit[1]} \t {investment_to_edit[3]} \t {investment_to_edit[4]*100}% \t\t {investment_to_edit[5]} \t\t {int(investment_to_edit[6] * 100 + 0.9999)/100}"
    )

    item = input("Re-enter name of investment: ")
    year_invested = input("Re-enter start year of the investment: ")
    principal = float(input("Re-enter investment amount in USD: "))
    interest = float(input("Re-enter interest rate in percent: ")) / 100
    year_maturity = input("Re-enter maturity year of the investment: ")
    future_value = principal * pow(
        (1 + interest), (int(year_maturity) - int(year_invested))
    )

    conn = sqlite3.connect(INVESTMENTS_DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        UPDATE investments
        SET item = ?, year_invested = ?, principal = ?, interest = ?, year_maturity = ?, future_value = ?
        WHERE id = ?
        """,
        (
            item,
            year_invested,
            principal,
            interest,
            year_maturity,
            future_value,
            item_id,
        ),
    )

    conn.commit()
    conn.close()
    clear()


def delete_investment():
    global recent_investments
    while True:
        display_recent_investments()
        print("What investment you wanted to delete?")
        selection = input("Enter number from 1 to 5: ")

        if 0 < int(selection) <= len(recent_investments):
            confirm = input("Are you sure to delete? (Enter either Y or N): ")
            if confirm == "Y" or confirm == "y":
                item_id = recent_investments[int(selection) - 1][0]

                conn = sqlite3.connect(INVESTMENTS_DB_PATH)
                c = conn.cursor()
                c.execute(
                    """
                    DELETE FROM investments
                    WHERE id = ?
                    """,
                    (item_id,),
                )
                conn.commit()
                conn.close()

                clear()
                print("Successfully deleted the item!")
                break
        else:
            print("Investment does not exist! Please try again.")


def investments(user_id_passed):
    global user_id
    user_id = user_id_passed
    while True:
        display_recent_investments()

        print(
            """
What would you want to do today?
            
1 - Add a new investment
2 - Edit recent investment
3 - Delete a recent investment
4 - Go back to menu
        """
        )

        match input("Your selection: "):
            case "1":
                add_investment()
            case "2":
                clear()
                edit_investment()
            case "3":
                clear()
                delete_investment()
            case "4":
                clear()
                return None
            case _:
                print("Enter a valid number!")
