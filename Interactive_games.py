FULL_TABLE = ["Civilian", "Civilian", "Civilian", "Civilian", "Civilian", "Civilian", "Sherif", "Don", "Mafia", "Mafia"]
NINE_PEOPLE_TABLE = ["Civilian", "Civilian", "Civilian", "Civilian", "Civilian", "Sherif", "Don", "Mafia", "Mafia"]
EIGHT_PEOPLE_TABLE = ["Civilian", "Civilian", "Civilian", "Civilian", "Civilian", "Sherif", "Don", "Mafia"]


def generate_table(a: int) -> dict:
    """Generate roles for 10, 9 or 8 people"""
    # globalise lists of roles
    global FULL_TABLE, NINE_PEOPLE_TABLE, EIGHT_PEOPLE_TABLE
    # aliases and its roles in the game
    roles = {}
    # for checking if host did not enter more mafias or more civilians than it can be
    possible_roles = FULL_TABLE if a == 10 else NINE_PEOPLE_TABLE if a == 9 else EIGHT_PEOPLE_TABLE

    #
    while len(possible_roles) > 0:
        alias, role = input("Enter the alias then role of this player ").split()
        if alias[0] != '@' or alias in roles or role not in possible_roles:
            print("Wrong enter: the alias of player already exist in the game or it was written incorrectly.\nEnter the alias and role again.")
            continue

        roles[alias] = role
        possible_roles.remove(role)

    return roles


def start_game() -> None:
    """Players take roles, save aliases of players"""
    players: dict

    number_of_players: int = int(input("Enter number of players in the game (from 8 to 10): "))
    if 8 <= number_of_players <= 10:
        players = generate_table(number_of_players)
    else:
        print("The game is not balanced, it will be unranked.")
        return

    print(players)
    return players


if __name__ == "__main__":
    start_game()
