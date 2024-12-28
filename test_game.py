import asyncio
from main import Game, Player
import random

class TestScenario:
    def __init__(self, name, players_count):
        self.name = name
        self.players_count = players_count
        self.game = Game(chat_id=123456789)
        self.players = []
        
    async def setup(self):
        # O'yinchilarni yaratish
        names = ["Ali", "Vali", "Gani", "Soli", "Toshmat", "Eshmat", "Pulat", "Aziz", "Jamshid", "Botir"]
        for i in range(self.players_count):
            player = Player(id=i+1, name=names[i], username=f"user{i+1}")
            self.players.append(player)
            self.game.players.append(player)
            
        # Rollarni taqsimlash
        self.game.game_mode = "classic"
        success = self.game.assign_roles()
        print(f"\n=== {self.name} ===")
        print(f"O'yinchilar soni: {self.players_count}")
        print(f"Rollar taqsimlandi: {success}")
        
        # Rollarni ko'rsatish
        roles_count = {}
        for player in self.game.players:
            role = self.game.roles.get(player.id)
            roles_count[role] = roles_count.get(role, 0) + 1
            print(f"{player.name}: {role}")
        print("\nRollar soni:")
        for role, count in roles_count.items():
            print(f"{role}: {count}")
            
        return success

class GameTester:
    def __init__(self):
        self.scenarios = []
        
    def add_scenario(self, scenario):
        self.scenarios.append(scenario)
        
    async def run_night_phase(self, game):
        print("\n=== TUN FAZASI ===")
        game.phase = "night"
        game.night_count += 1
        print(f"Tun {game.night_count} boshlandi")
        
        # Mafiya harakati
        mafia_players = [p for p in game.players if game.roles[p.id] == "Mafia" and p.is_alive]
        for mafia in mafia_players:
            possible_targets = [p for p in game.players if p.id != mafia.id and p.is_alive]
            if possible_targets:
                target = random.choice(possible_targets)
                game.mafia_votes[mafia.id] = target.id
                print(f"Mafiya harakati: {mafia.name} -> {target.name}")
        
        # Doktor harakati
        doctor = next((p for p in game.players if game.roles[p.id] == "Doctor" and p.is_alive), None)
        if doctor:
            possible_targets = [p for p in game.players if p.is_alive]
            if possible_targets:
                target = random.choice(possible_targets)
                game.doctor_target = target.id
                print(f"Doktor harakati: {doctor.name} -> {target.name}")
        
        # Detektiv harakati
        detective = next((p for p in game.players if game.roles[p.id] == "Detective" and p.is_alive), None)
        if detective:
            possible_targets = [p for p in game.players if p.id != detective.id and p.is_alive]
            if possible_targets:
                target = random.choice(possible_targets)
                game.detective_target = target.id
                target_role = game.roles[target.id]
                is_mafia = target_role in ["Mafia", "Traitor"]
                print(f"Detektiv harakati: {detective.name} -> {target.name} ({target_role})")
        
        # Tun natijalarini hisoblash
        vote_counts = {}
        for target_id in game.mafia_votes.values():
            vote_counts[target_id] = vote_counts.get(target_id, 0) + 1
        
        if vote_counts:
            target_id = max(vote_counts.items(), key=lambda x: x[1])[0]
            target = game.get_player_by_id(target_id)
            protected = target_id == game.doctor_target
            
            print(f"\nTun natijalari:")
            if protected:
                print(f" {target.name} himoyalandi!")
            else:
                target.is_alive = False
                print(f" {target.name} o'ldirildi!")
                
        # Tirik o'yinchilarni ko'rsatish
        alive_players = game.get_alive_players()
        print(f"\nTirik o'yinchilar ({len(alive_players)}):")
        for player in alive_players:
            role = game.roles[player.id]
            print(f"{player.name} ({role})")
            
    async def run_day_phase(self, game):
        print("\n=== KUN FAZASI ===")
        game.phase = "day"
        game.day_count += 1
        print(f"Kun {game.day_count} boshlandi")
        
        # Tirik o'yinchilar ovoz beradi
        alive_players = game.get_alive_players()
        for voter in alive_players:
            possible_targets = [p for p in alive_players if p.id != voter.id]
            if possible_targets:
                target = random.choice(possible_targets)
                game.votes[voter.id] = target.id
                print(f"Ovoz: {voter.name} -> {target.name}")
        
        # Ovoz berish natijalarini hisoblash
        vote_counts = {}
        for target_id in game.votes.values():
            vote_counts[target_id] = vote_counts.get(target_id, 0) + 1
        
        if vote_counts:
            most_voted = max(vote_counts.items(), key=lambda x: x[1])[0]
            voted_player = game.get_player_by_id(most_voted)
            voted_player.is_alive = False
            print(f"\nOvoz berish natijalari:")
            print(f" {voted_player.name} ({vote_counts[most_voted]} ovoz) o'ldirildi!")
            
        # Tirik o'yinchilarni ko'rsatish
        alive_players = game.get_alive_players()
        print(f"\nTirik o'yinchilar ({len(alive_players)}):")
        for player in alive_players:
            role = game.roles[player.id]
            print(f"{player.name} ({role})")
            
        # G'olibni aniqlash
        mafia_count = len([p for p in alive_players if game.roles[p.id] == "Mafia"])
        citizen_count = len([p for p in alive_players if game.roles[p.id] != "Mafia"])
        
        if mafia_count == 0:
            print("\n FUQAROLAR G'ALABA QILDI!")
            return True
        elif mafia_count >= citizen_count:
            print("\n MAFIYA G'ALABA QILDI!")
            return True
        return False
            
    async def run_all_tests(self):
        for scenario in self.scenarios:
            success = await scenario.setup()
            if not success:
                print(f"XATO: {scenario.name} - Rollar taqsimlanmadi")
                continue
                
            game_over = False
            max_rounds = 10
            current_round = 0
            
            while not game_over and current_round < max_rounds:
                current_round += 1
                print(f"\n=== RAUND {current_round} ===")
                
                await self.run_night_phase(scenario.game)
                game_over = await self.run_day_phase(scenario.game)
                
                if game_over:
                    print(f"\nO'yin {current_round} raundda tugadi")
                elif current_round == max_rounds:
                    print("\nMAKSIMAL RAUND SONI TUGADI")

async def main():
    tester = GameTester()
    
    # Turli xil o'yinchi sonlari bilan test qilish
    player_counts = [4, 5, 6, 7, 8, 9, 10]
    for count in player_counts:
        scenario = TestScenario(f"Test {count} o'yinchi", count)
        tester.add_scenario(scenario)
    
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
