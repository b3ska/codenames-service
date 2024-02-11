from fastapi import WebSocket

class Player:
    def __init__(self, uid: str, auth:str, ws: WebSocket):
        self.uid = uid
        self.ws = ws

    async def send_msg(self, message: str):
        await self.ws.send_text(message)

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

    def send_msg_to_all(self, message: str):
        for player in self.players:
            player.send_msg(message)
    
    def send_msg_to_player(self, uid: str, message: str):
        for player in self.players:
            if player.uid == uid:
                player.send_msg(message)

    def close(self):
        self.send_msg_to_all(str({"msg":"The lobby has been closed."}))
        for player in self.players:
            player.close()
        self.players = []
        self.status = "closed"

    async def start_game(self, start_game: function):
        if self.host:
            await self.host.send_msg("Starting the game!")
        else:
            print("No host to start the game!")
