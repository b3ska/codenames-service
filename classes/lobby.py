import random
from classes.field import Field
from classes.player import Player

class Lobby:
    def __init__(self, expected_players: list[str]):
        self.players = []
        self.host = None
        self.status = "in_progress"
        self.exptected_players = expected_players

    def add_player(self, player: Player):
        self.players.append(player)
        self.send_msg_to_all(str({"msg":"Joined the lobby.", "uid":player.uid}))

    def set_host(self, uid: str):
        for player in self.players:
            if player.uid == uid:
                self.host = player
                break

    def remove_player(self, uid: str):
        self.players = [player for player in self.players if player.uid != uid]
        self.send_msg_to_all(str({"msg":"Left the lobby.", "uid":uid}))
        if (self.players == []):
            self.status = "empty"

    def send_msg_to_all(self, message: str, type_: str, uid = ""):
        for player in self.players:
            player.send_msg(str({
                "msg": message,
                "type": type_,
                "uid": uid
            }))
    
    def send_msg_to_player(self, to_uid: str, message: str, type_: str, from_uid = ""):
        for player in self.players:
            if player.uid == to_uid:
                player.send_msg(str({
                    "msg": message,
                    "type": type_,
                    "uid": from_uid
                }))

    def close(self):
        self.send_msg_to_all(str({"msg":"The lobby has been closed."}))
        for player in self.players:
            player.close()
        self.players = []
        self.status = "closed"

    async def start_game(self, uid: str):
        if self.host.uid == uid:
            await self.send_msg_to_all("game has started", "move", self.host.uid)
            self.status = "in_progress"
            self.score = {"red": 0, "blue": 0}
            self.field = Field()
            self.playing_team = random.choice(["red", "blue"])
            self.waiting_team = "red" if self.playing_team == "blue" else "blue"
            while self.status == "in_progress":
                await self.handle_round()
            
    async def handle_round(self):
        playing_team, waiting_team = waiting_team, playing_team
        await self.send_msg_toall(self.field, "field")
        data = await self.spymaster_turn()
        await self.send_msg_toall(data, "hint")
        
        
    async def spymaster_turn(self):
        for player in self.players:
            if player.team == self.playing_team and player.role == "spymaster":
                await self.send_msg_to_all(player.uid+"'s move to send hint", "move")
                data = await player.get_player_input() # waiting for json {"hint": "test", "num_guesses": 2}
                return data
        return None
    
    async def agent_turn(self, move: str, uid: str):
        agents = []
        for player in self.player:
            if player.team == self.playing_team and player.role == "agent":
                agents.append(player)
                
        await self.send_msg_toall(str(map(lambda x: x.uid + " ", agents))+" move", "move")
        if data is not None and "num_guesses" in data:
            for i in range(data["num_guesses"]):
                data = await agents[0].get_player_input()  # waiting for json {"x": 0, "y": 0}
                if not data: break
                x, y = data["x"], data["y"]
                self.field.toggle_revealed(x, y)
                if self.field.get_card(x, y).color == self.playing_team:
                    self.score[self.playing_team] += 1
                elif self.field.get_card(x, y).color == self.waiting_team:
                    self.score[self.waiting_team] += 1
                    break
                elif self.field.get_card(x, y).color == "black":
                    self.score[self.waiting_team] = self.field.num_colored
                    break
                else:
                    break
                await self.send_msg_to_all(self.field, "field")
                
        await self.send_msg_to_all(self.score, "score")
        if (self.score["red"] == self.field.num_colored or self.score["blue"] == self.field.num_colored): 
            self.status = "finished"
            return
                    
    def handle_move(self, move: str, uid: str):
        self.send_msg_to_all(move, "move", uid)

    def handle_game_state(self, game_state: str, uid: str):
        if game_state == "in_progress":
            self.start_game(uid)
    
    def info_handler():
        pass
    
    
        
        
        

        
