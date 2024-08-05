from modules.clear import clear
from modules.transactions import transactions
from modules.budget import budget
from modules.investments import investments


def menu(user_id):
    while True:
        print(
            """What do you want to do today?

1 - Add/edit Income or Expense
2 - Set and edit a budget
3 - Manage Investments
4 - Reports
5 - Logout and exit
        """
        )
        action = input("Your selection: ")
        clear()
        match action:
            case "1":
                transactions(user_id)
            case "2":
                budget(user_id)
            case "3":
                investments(user_id)
            case "4":
                print("case 4")
            case "5":
                print("Successfully logged out. Thank you for coming!")
                return None
            case _:
                print("Enter a valid number!")
