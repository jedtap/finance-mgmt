from modules.clear import clear


def selection():
    while True:
        print(
            """
What do you want to do today?

1 - Add new Income/Expense
2 - Set a budget
3 - Manage Investments
4 - Reports
5 - Logout and exit
        """
        )
        action = input("Your selection: ")
        clear()
        if action == "1" or action == "2":
            break
        else:
            print("Invalid selection, please try again.")
    return action


def menu(user_id):
    while True:
        print(
            """
What do you want to do today?

1 - Add new Income/Expense
2 - Set a budget
3 - Manage Investments
4 - Reports
5 - Logout and exit
        """
        )
        action = input("Your selection: ")
        clear()
        match action:
            case "1":
                print("case 1")
            case "2":
                print("case 2")
            case "3":
                print("case 3")
            case "4":
                print("case 4")
            case "5":
                print("Successfully logged out. Thank you for coming!")
                return None
            case _:
                print("enter a valid number!")
