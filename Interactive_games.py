from random import randint
from colorama import Fore, Back

FULL_TABLE = ["Мирный", "Мирный", "Мирный", "Мирный", "Мирный", "Мирный", "Шериф", "Дон", "Мафия", "Мафия"]
NINE_PEOPLE_TABLE = ["Мирный", "Мирный", "Мирный", "Мирный", "Мирный", "Шериф", "Дон", "Мафия", "Мафия"]
EIGHT_PEOPLE_TABLE = ["Мирный", "Мирный", "Мирный", "Мирный", "Мирный", "Шериф", "Дон", "Мафия"]
LIST_FOR_GAMES = {8: EIGHT_PEOPLE_TABLE, 9: NINE_PEOPLE_TABLE, 10: FULL_TABLE}


def generate_table(a: int) -> list:
    """Generate roles for 10, 9 or 8 people"""

    global LIST_FOR_GAMES
    default = LIST_FOR_GAMES[a]  # sorted list of roles
    roles = []  # final list of roles

    # generate random list of roles
    for j in range(10):
        x = default[randint(0, len(default) - 1)]
        roles.append(x)
        default.remove(x)

    return roles


def game():
    play = True
    while play:
        roles = generate_table()

        print(Fore.CYAN + "Роли игроков:")

        for i in range(len(roles)):
            match roles[i]:
                case "Мафия": color, back = Fore.BLACK, Back.WHITE
                case "Шериф": color, back = Fore.YELLOW, Back.RESET
                case "Дон": color, back = Fore.WHITE, Back.BLACK
                case _: color, back = Fore.RED, Back.RESET
            print(color + back + "Игрок номер {:d}: {:s}".format(i + 1, roles[i]))

        if not ("да" in input(Fore.CYAN + "Новая игра?").lower()):
            print("Завершение мафии")
            play = False


if __name__ == "__main__":
    game()
