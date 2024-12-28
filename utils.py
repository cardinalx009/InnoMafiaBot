import random
from typing import Dict, List, Tuple

# O'yin uchun rasmlar
ROLE_IMAGES = {
    "citizen": "https://i.imgur.com/nX5DMTL.png",    # Fuqaro
    "mafia": "https://i.imgur.com/K2K9GvP.png",      # Mafiya
    "doctor": "https://i.imgur.com/YZ8fVwR.png",     # Shifokor
    "detective": "https://i.imgur.com/P8k9DmN.png",  # Detektiv
    "bodyguard": "https://i.imgur.com/VrJ4QzL.png",  # Qo'riqchi
    "maniac": "https://i.imgur.com/H7kZvTp.png",     # Telba
    "journalist": "https://i.imgur.com/WqN9ZxM.png", # Jurnalist
    "bomber": "https://i.imgur.com/B5X2Qn4.png",     # Bombachi
    "ninja": "https://i.imgur.com/Lq8RXJK.png",      # Ninja
    "don": "https://i.imgur.com/9mK2YzP.png"         # Don
}

GAME_IMAGES = {
    "welcome": "https://i.imgur.com/ZNwxPdQ.png",   # Kirish rasmi
    "night": "https://i.imgur.com/K9m4LqY.png",     # Tun
    "day": "https://i.imgur.com/R8YtxdK.png",       # Kun
    "vote": "https://i.imgur.com/XcMPvDN.png",      # Ovoz berish
    "shop": "https://i.imgur.com/YwP9BVg.png",      # Do'kon
}

# Do'kon mahsulotlari
SHOP_ITEMS = {
    "extra_life": {
        "name": " Qo'shimcha jon",
        "description": "O'lganingizda bir marta qayta tirilish imkoniyati",
        "price": 1000,
        "image": "https://i.imgur.com/YQeD1Nh.png"
    },
    "role_change": {
        "name": " Rol almashtirish",
        "description": "O'yin boshida rolni qayta tanlash imkoniyati",
        "price": 2000,
        "image": "https://i.imgur.com/8BH4L6d.png"
    },
    "vote_shield": {
        "name": " Ovoz qalqoni",
        "description": "Bir marta ovoz berishdan himoyalanish",
        "price": 1500,
        "image": "https://i.imgur.com/JYgKkbY.png"
    },
    "double_vote": {
        "name": " Ikkilangan ovoz",
        "description": "Ovoz berishda ovozingiz 2 marta hisoblanadi",
        "price": 1800,
        "image": "https://i.imgur.com/qF5s9TP.png"
    }
}

class Role:
    CITIZEN = "citizen"      # Fuqaro
    MAFIA = "mafia"         # Mafiya
    DOCTOR = "doctor"       # Shifokor
    DETECTIVE = "detective" # Detektiv
    BODYGUARD = "bodyguard" # Qo'riqchi
    MANIAC = "maniac"       # Telba
    JOURNALIST = "journalist" # Jurnalist
    BOMBER = "bomber"       # Bombachi
    NINJA = "ninja"         # Ninja
    DON = "don"            # Don (Mafiya boshlig'i)

    @staticmethod
    def get_description(role: str) -> str:
        descriptions = {
            Role.CITIZEN: "👥 Fuqaro - Shaharni himoya qiling! Kunduzi mafiyani topish uchun ovoz bering, kechasi esa ehtiyot bo'ling!",
            Role.MAFIA: "🔪 Mafiya - Tunlari birlashib fuqarolarni yo'q qiling! Kunduzi esa o'zingizni oddiy fuqarodek ko'rsating!",
            Role.DOCTOR: "💉 Shifokor - Har tun bir kishini davolash imkoniyatingiz bor. O'zingizni ketma-ket ikki marta davolay olmaysiz!",
            Role.DETECTIVE: "🔍 Detektiv - Har tun bir kishining rolini tekshirish imkoniyatingiz bor. Natijani faqat o'zingiz ko'rasiz!",
            Role.BODYGUARD: "🛡️ Qo'riqchi - Har tun bir kishini himoya qilasiz. Himoyalangan kishi tungi hujumlardan omon qoladi!",
            Role.MANIAC: "🔪 Telba - Har tun bir kishini o'ldirish imkoniyatingiz bor. Siz yolg'iz o'ynaysiz, hech kim bilan hamkorlik qilmaysiz!",
            Role.JOURNALIST: "📰 Jurnalist - Har tun bir o'yinchi haqida ma'lumot olasiz. Bu ma'lumotni boshqalar bilan bo'lishish yoki yashirish sizning qo'lingizda!",
            Role.BOMBER: "💣 Bombachi - O'lganingizda o'zingiz bilan birga bir kishini portlatib yuborasiz. Portlash qurbonini oldindan tanlaysiz!",
            Role.NINJA: "🥷 Ninja - Har tun bir kishini ovoz berishdan to'xtatish imkoniyatingiz bor. Bu kishi keyingi kun ovoz bera olmaydi!",
            Role.DON: "👑 Don - Mafiya boshlig'i, har tun kimnidir o'ldirish VA bir kishining rolini tekshirish imkoniyatingiz bor!"
        }
        return descriptions.get(role, "Noma'lum rol")

    @staticmethod
    def get_team(role: str) -> str:
        mafia_team = {Role.MAFIA, Role.DON}
        neutral_team = {Role.MANIAC, Role.BOMBER}
        
        if role in mafia_team:
            return "mafia"
        elif role in neutral_team:
            return "neutral"
        else:
            return "citizen"

def distribute_roles(player_count: int) -> List[str]:
    """O'yinchilar soniga qarab rollarni taqsimlash"""
    if player_count < 4:
        raise ValueError("O'yin boshlash uchun kamida 4 ta o'yinchi kerak!")
        
    roles = []
    
    # Asosiy rollar (har doim bo'ladi)
    roles.extend([Role.DOCTOR, Role.DETECTIVE])
    
    # O'yinchilar soniga qarab qo'shimcha rollar
    if player_count >= 6:
        roles.append(Role.BODYGUARD)
    if player_count >= 8:
        roles.append(Role.JOURNALIST)
    if player_count >= 10:
        roles.append(Role.NINJA)
    if player_count >= 12:
        roles.append(Role.BOMBER)
    
    # Mafiya va Don
    if player_count <= 6:
        roles.append(Role.MAFIA)
    elif player_count <= 9:
        roles.extend([Role.MAFIA, Role.DON])
    elif player_count <= 12:
        roles.extend([Role.MAFIA, Role.MAFIA, Role.DON])
    else:  # 13-15 o'yinchi
        roles.extend([Role.MAFIA, Role.MAFIA, Role.MAFIA, Role.DON])
    
    # Telba (tasodifiy)
    if player_count >= 7 and random.random() < 0.3:  # 30% ehtimol
        roles.append(Role.MANIAC)
    
    # Qolgan o'yinchilar fuqaro bo'ladi
    citizen_count = player_count - len(roles)
    roles.extend([Role.CITIZEN] * citizen_count)
    
    # Rollarni aralashtirish
    random.shuffle(roles)
    return roles

def format_player_list(players: Dict, show_roles: bool = False, show_status: bool = True) -> str:
    """O'yinchilar ro'yxatini chiroyli formatda qaytaradi"""
    if not players:
        return "O'yinchilar yo'q"
        
    result = []
    for user_id, player in players.items():
        status = ""
        if show_status:
            if not player["alive"]:
                status = "☠️ "
            elif player.get("protected", False):
                status = "🛡️ "
            else:
                status = "✅ "
                
        name = player["username"]
        if show_roles and player["role"]:
            role_icons = {
                Role.CITIZEN: "👨‍💼",
                Role.MAFIA: "🕴️",
                Role.DOCTOR: "👨‍⚕️",
                Role.DETECTIVE: "🕵️",
                Role.BODYGUARD: "💂‍♂️",
                Role.MANIAC: "🔪",
                Role.JOURNALIST: "📰",
                Role.BOMBER: "💣",
                Role.NINJA: "🥷",
                Role.DON: "👑"
            }
            name = f"{role_icons.get(player['role'], '❓')} {name}"
        result.append(f"{status}{name}")
    
    return "\n".join(sorted(result))

def create_player_stats() -> Dict:
    """O'yinchi statistikasini yaratish"""
    return {
        "total_games": 0,
        "wins": {
            "citizen": 0,
            "mafia": 0,
            "neutral": 0
        },
        "roles_played": {
            "citizen": 0,
            "mafia": 0,
            "doctor": 0,
            "detective": 0,
            "bodyguard": 0,
            "maniac": 0,
            "journalist": 0,
            "bomber": 0,
            "ninja": 0,
            "don": 0
        },
        "coins": 0,
        "inventory": {
            "extra_life": 0,
            "role_change": 0,
            "vote_shield": 0,
            "double_vote": 0
        }
    }

def update_player_coins(stats: Dict, amount: int) -> Dict:
    """O'yinchi tangalarini yangilash"""
    stats["coins"] = max(0, stats["coins"] + amount)
    return stats

def format_shop_items() -> str:
    """Do'kon mahsulotlarini chiroyli formatda qaytaradi"""
    shop_text = " NightShadow Mafia do'koni\n\n"
    for item_id, item in SHOP_ITEMS.items():
        shop_text += f"{item['name']} - {item['price']} tanga\n"
        shop_text += f" {item['description']}\n\n"
    return shop_text

def can_buy_item(stats: Dict, item_id: str) -> bool:
    """O'yinchi mahsulotni sotib olishi mumkinligini tekshiradi"""
    if item_id not in SHOP_ITEMS:
        return False
    return stats["coins"] >= SHOP_ITEMS[item_id]["price"]

def buy_item(stats: Dict, item_id: str) -> Tuple[bool, str]:
    """Mahsulotni sotib olish"""
    if not can_buy_item(stats, item_id):
        return False, "Sizda yetarli tanga mavjud emas!"
        
    price = SHOP_ITEMS[item_id]["price"]
    stats["coins"] -= price
    stats["inventory"][item_id] += 1
    
    return True, f"{SHOP_ITEMS[item_id]['name']} sotib olindi! (-{price} tanga)"

def format_player_stats(stats: Dict) -> str:
    """O'yinchi statistikasini chiroyli formatda qaytaradi"""
    roles_text = "\n".join([
        f"{Role.get_description(role).split(' - ')[0]}: {count}"
        for role, count in stats["roles_played"].items()
        if count > 0
    ])
    
    inventory_text = "\n".join([
        f"{SHOP_ITEMS[item]['name']}: {count}"
        for item, count in stats["inventory"].items()
        if count > 0
    ])
    
    return f""" O'yinchi statistikasi:

 Tangalar: {stats['coins']}

 Jami o'yinlar: {stats['total_games']}

 G'alabalar:
 Fuqarolar: {stats['wins']['citizen']}
 Mafiya: {stats['wins']['mafia']}
 Betaraf: {stats['wins']['neutral']}

 O'ynalgan rollar:
{roles_text}

 Inventar:
{inventory_text or "Bo'sh"}"""

SHOP_ITEMS = {
    "extra_life": {
        "name": " Qo'shimcha jon",
        "description": "O'lganingizda bir marta qayta tirilish imkoniyati",
        "price": 1000,
        "image": "https://i.imgur.com/YQeD1Nh.png"
    },
    "role_change": {
        "name": " Rol almashtirish",
        "description": "O'yin boshida rolni qayta tanlash imkoniyati",
        "price": 2000,
        "image": "https://i.imgur.com/8BH4L6d.png"
    },
    "vote_shield": {
        "name": " Ovoz qalqoni",
        "description": "Bir marta ovoz berishdan himoyalanish",
        "price": 1500,
        "image": "https://i.imgur.com/JYgKkbY.png"
    },
    "double_vote": {
        "name": " Ikkilangan ovoz",
        "description": "Ovoz berishda ovozingiz 2 marta hisoblanadi",
        "price": 1800,
        "image": "https://i.imgur.com/qF5s9TP.png"
    }
}
