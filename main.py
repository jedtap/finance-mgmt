from modules.initialize import initialize
from modules.authentication import authentication
from modules.menu import menu

def main():
    initialize()
    user_id = authentication()
    menu(user_id)

main()
