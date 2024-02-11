from player import Player

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

    async def start_game(self, start_game: function):
        if self.host:
            await self.send_msg_to_all("game has started", "move", self.host.uid)
        else:
            print("No host to start the game!")
