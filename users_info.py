from pyrebase import initialize_app
import dotenv
from os import getenv

dotenv.load_dotenv(dotenv.find_dotenv())

DATA: dict = {
    "apiKey": getenv("apiKey"),
    "authDomain": getenv("authDomain"),
    "databaseURL": getenv("databaseURL"),
    "projectId": getenv("projectId"),
    "storageBucket": getenv("storageBucket"),
    "messagingSenderId": getenv("messagingSenderId"),
    "appId": getenv("appId"),
    "measurementId": getenv("measurementId")
}


def import_string() -> str:
    return initialize_app(DATA).database().child("save").get().val()


def parse_data(string: str = "") -> dict:
    players: dict[dict] = {}

    substring = string.split(";")

    for player in substring[:-1]:
        alias, player_id, name, points = player.split(":")
        players[alias] = {"name": name, "id": player_id, "points": points}

    return players


if __name__ == "__main__":
    print(parse_data(import_string()))
