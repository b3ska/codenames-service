import asyncio
import random
import websockets
import json
from classes.Card import Card
from classes.Player import SpyMaster
from classes.Player import Agent
from classes.Field import Field

LOBBYS = {
    1238: {
        "allowed_games": {0 : "CodeNames"},
        "code" : "0051",
        "desc" : "This IS CODENAMES",
        "game" : "Truth or Dare",
        "host" : "372aK76mbQURxTXoRPSOG8dTP0V2",
        "maxPlayers" : 10,
        "minPlayers": 4,
        "players" : {
            0 : "372aK76mbQURxTXoRPSOG8dTP0V2",
            1 : "rbERfRUndSRizl3Sds6Al8lTJOp1",
            2 : "mPxbBKrDQQYKEXuxqZJc8ffApgo1",
        },
        "status" : "started",
    },
    "Second lobby data" : {},
}

PLAYERS = {}
FIELDS = {}

async def send_field(socket_list, field):
    for player in socket_list:
        await player.send_field(field)
        
def log_game_moves(log, lobby_id):
    try:
        with open(f"{lobby_id}_game_log.txt", "a") as f:
            f.write(log + "\n")
    except FileNotFoundError:
        with open(f"{lobby_id}_game_log.txt", "w") as f:
            f.write(log + "\n")
        
async def find_full_lobby():
    while True:
        for lobby_id, lobby_data in LOBBYS.items():
            if "players" in lobby_data and lobby_id in PLAYERS.keys():
                if len(lobby_data["players"]) == len(PLAYERS[lobby_id]):
                    print("Full lobby found.")
                    await game(PLAYERS[lobby_id], FIELDS[lobby_id], lobby_id)
        await asyncio.sleep(5)

async def game(socket_list, field, lobby_id):
    score = {"red": 0, "blue": 0}
    
    log_game_moves("Game started.", lobby_id)
    # send field to all players
    playing_team = random.choice(socket_list).team
    waiting_team = "red" if playing_team == "blue" else "blue"
    print("playing team:", playing_team)
    
    while True:
        playing_team, waiting_team = waiting_team, playing_team
        await send_field(socket_list, field)
        log_game_moves(f"Playing team: {playing_team}", lobby_id)
        log_game_moves(str(field), lobby_id)
        data = None
        
        for player in socket_list:
            if player.team == playing_team and isinstance(player, SpyMaster):
                log_game_moves(f"{player.name}'s turn to send .", lobby_id)
                await player.send_data("your turn")
                data = await player.recieve_data()
            else: 
                await player.send_data("turn : " + playing_team)
        
        #send hint to all players
        for player in socket_list:
            await player.send_data(data)

        log_game_moves(f"Hint: {data['hint']}, {data['num_guesses']}", lobby_id)
        
        for player in socket_list:
            if player.team == playing_team and isinstance(player, Agent):
                await player.send_data("send guess cards")
                if data is not None and "num_guesses" in data:
                    for i in range(data["num_guesses"]):
                        data = await player.recieve_data()
                        if not data: break
                        x, y = data["x"], data["y"]
                        log_game_moves(f"{player.name} guessed {str(field.get_card(x, y))}.", lobby_id)
                        field.toggle_revealed(x, y)
                        if field.get_card(x, y).color == playing_team:
                            score[playing_team] += 1
                        elif field.get_card(x, y).color == waiting_team:
                            score[waiting_team] += 1
                            break
                        elif field.get_card(x, y).color == "black":
                            score[waiting_team] = field.num_colored
                            break
                        await send_field(socket_list, field)
        
        log_game_moves(f"Score: {score}", lobby_id)
        if (score["red"] == field.num_colored or score["blue"] == field.num_colored): break
        print("score:", score)
        
    # end game
    for player in socket_list:
        await player.send_data("game over")
        await player.send_data(score)
        player.socket.close()
        
    log_game_moves("Game over.", lobby_id)

async def handler(websocket, path):
    # do something upon connection
    await websocket.send("Hello from the server!")

    lobby_containing_player = {}
    lobby_id_containing_player = None
    
    # wait for data
    data = await websocket.recv()   # waiting for json {"name": "Artem1", "role": "SpyMaster", "uid": "372aK76mbQURxTXoRPSOG8dTP0V2", "team": "red"}
    try:
        data = json.loads(data)
    except json.decoder.JSONDecodeError:
        await websocket.send("Invalid data.")
        websocket.close()

    # find lobby containing player
    for lobby_id, lobby_data in LOBBYS.items():
        if "players" in lobby_data and data['uid'] in lobby_data["players"].values():
            lobby_containing_player = LOBBYS[lobby_id]
            lobby_id_containing_player = lobby_id
            break
    
    if not lobby_id_containing_player:
        await websocket.send("Lobby not found.")
        websocket.close()
        return
    
    # add player to socket list
    if not PLAYERS.get(lobby_id_containing_player):
        if data["role"] == "spymaster": PLAYERS[lobby_id_containing_player] = [SpyMaster(data["name"], data["team"], websocket)]
        elif data["role"] == "agent": PLAYERS[lobby_id_containing_player] = [Agent(data["name"], data["team"], websocket)]
    else:
        if data["role"] == "spymaster": PLAYERS[lobby_id_containing_player].append(SpyMaster(data["name"], data["team"], websocket))
        elif data["role"] == "agent": PLAYERS[lobby_id_containing_player].append(Agent(data["name"], data["team"], websocket))
    
    connected_players = len(PLAYERS[lobby_id_containing_player])

    # wait for everyone to connect
    log_game_moves(f"{data['name']} connected.", lobby_id_containing_player)
    await websocket.send("Waiting for everyone to connect...")
    while connected_players < len(lobby_containing_player["players"]):
        await asyncio.sleep(3)
        connected_players = len(PLAYERS[lobby_id_containing_player])
    
    if connected_players == len(lobby_containing_player["players"]):
        if not FIELDS.get(lobby_id_containing_player):
            FIELDS[lobby_id_containing_player] = Field()
            
    try:
        await websocket.wait_closed()
    finally:
        print("Connection closed.")
        # remove player from socket list




async def main():
    async with websockets.serve(handler, "localhost", 8081):
        await find_full_lobby()

if __name__ == "__main__":
    asyncio.run(main())