from pyrebase import initialize_app

DATA: dict = {"apiKey": "AIzaSyBVugd2_hqpJ6oyxW3mjF8jthIYM_80yyA",
              "authDomain": "innomafiaapp.firebaseapp.com",
              "databaseURL": "https://innomafiaapp-default-rtdb.europe-west1.firebasedatabase.app",
              "projectId": "innomafiaapp",
              "storageBucket": "innomafiaapp.appspot.com",
              "messagingSenderId": "120476741929",
              "appId": "1:120476741929:web:132dc5a5f76a6e14394738",
              "measurementId": "G-0LMQQNBN7N"}


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
