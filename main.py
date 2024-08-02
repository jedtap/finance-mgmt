from modules.initialize import initialize
from modules.authentication import authentication


def main():
    initialize()
    user_id = authentication()
    print(f'User {user_id[0]} is authenticated!')


main()
