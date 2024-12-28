"""
O'yinchilar haqida ma'lumotlarni olish.
"""
__author__ = "Zener085"
__version__ = "1.0.0"
__license__ = "MIT"

from pyrebase import initialize_app
from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

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


class Player:
    def __init__(self, *args: str):
        self.alias: str = str(args[0])
        self.id: int = int(args[1])
        self.name: str = str(args[2])
        self.points: int = int(args[3])
        self.loses: int = int(args[4])
        self.attendance: int = self.loses + self.points

    def __str__(self) -> str:
        return "Ism - " + self.name + \
               "\nID - " + str(self.id) + \
               "\nOchkolar - " + str(self.points) + \
               "\nMag'lubiyatlar - " + str(self.loses)

    def get_info(self) -> str:
        total_games = self.points + self.loses
        win_rate = round((self.points / total_games * 100), 2) if total_games > 0 else 0
        return (
            f" Statistika: {self.name}\n\n"
            f" Jami o'yinlar: {total_games}\n"
            f" G'alabalar: {self.points}\n"
            f" Mag'lubiyatlar: {self.loses}\n"
            f" G'alaba foizi: {win_rate}%"
        )

    def __repr__(self) -> str:
        return "Ism - " + self.name + \
               "; ID - " + str(self.id) + \
               "; Ochkolar - " + str(self.points) + \
               "; Mag'lubiyatlar - " + str(self.loses)


def import_string() -> str:
    """Ma'lumotlar bazasidan ma'lumotlarni olish"""
    return initialize_app(DATA).database().child("save").get().val()


def parse_data(string: str = None) -> dict:
    """Ma'lumotlarni qayta ishlash"""
    if string is None:
        return {}

    players: dict[str, Player] = {}

    for substring in string.split(";")[:-1]:
        player = Player(*substring.split(":"))
        players[player.alias] = player

    return players


def generate_top(top_: list) -> list:
    """Bir xil ochkoli top 3 o'yinchilarni ro'yxatini yaratish"""
    top_players: list = [[top_[0]]]
    index: int = 0

    for i in range(1, len(top_)):
        if top_[i].points == top_[i - 1].points:
            top_players[index].append(top_[i])
        else:
            players = 0
            for top_player in top_players:
                players += len(top_player)
            if players >= 3:
                break
            top_players.append([top_[i]])
            index += 1

    return top_players


def top_rating() -> str:
    """Top 3 yoki undan yuqori o'yinchilar ro'yxatini qaytarish"""
    answer = " Top o'yinchilar:\n\n"
    top: list = sorted(parse_data(import_string()).values(), key=lambda p: p.points, reverse=True)

    if not top:
        return " Hozircha o'yinchilar yo'q."

    if top[0].points == 0:
        return " Hamma o'yinchilarning ochkosi 0 ga teng."

    top = generate_top(top)
    
    if len(top) == 1:  # Barcha top 3 o'yinchilarning ochkolari bir xil
        answer += f" 1-{len(top[0])}: "
        for player in top[0]:
            answer += f"{player.name}, "
        answer = answer[:-2]  # oxiridagi vergul va bo'shliqni olib tashlash
        answer += f"\n Hammasi {top[0][0].points} ochkoga ega"
    else:
        medals = ["", "", ""]
        place = 1
        players_counted = 0
        
        for group in top:
            if players_counted >= 3:
                break
                
            if len(group) == 1:
                answer += f"{medals[place-1]} {place}-o'rin: {group[0].name} - {group[0].points} ochko\n"
            else:
                answer += f"{medals[place-1]} {place}-o'rin: "
                for player in group:
                    answer += f"{player.name}, "
                answer = answer[:-2]  # oxiridagi vergul va bo'shliqni olib tashlash
                answer += f" - {group[0].points} ochko\n"
                
            place += len(group)
            players_counted += len(group)

    return answer


if __name__ == "__main__":
    pass
