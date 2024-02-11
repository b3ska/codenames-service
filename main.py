# main file for codenames-service, runs the server and handles connections,
# also handles the game logic, and the game log.
from fastapi import FastAPI, WebSocket, Header
from typing import Annotated
import asyncio
import random
import json
from classes.lobby import Lobby, Player
from classes.card import Card
from classes.player import SpyMaster
from classes.player import Agent
from classes.field import Field
import clients.lobby_service as lobby_service

LOBBYS = {
    1238: {
        "allowed_games": {0 : "CodeNames"},
        "code" : "0051",
        "desc" : "This IS CODENAMES",
        "game" : "codenames",
        "host" : "372aK76mbQURxTXoRPSOG8dTP0V2",
        "maxPlayers" : 10,
        "minPlayers": 4,
        "players" : {
            0 : "372aK76mbQURxTXoRPSOG8dTP0V2",
            1 : "rbERfRUndSRizl3Sds6Al8lTJOp1",
            2 : "mPxbBKrDQQYKEXuxqZJc8ffApgo1",
            4 : "asdsdasdfaYKEXuxqZJc8ffAfgo2",
        },
        "status" : "doesnt matter",
    },
    "Second lobby data" : {},
}

players = {}
fields = {}

async def send_data_toall(socket_list, data):
    '''Sends the data to all players in the socket list.'''
    for player in socket_list:
        if isinstance(data, Field):
            await player.send_field(data)
        else:
            await player.send_data(data)
        
def log_game_moves(log, lobby_id):
    '''Logs game moves to a file.'''
    try:
        with open(f"{lobby_id}_game_log.txt", "a") as f:
            f.write(log + "\n")
    except FileNotFoundError:
        with open(f"{lobby_id}_game_log.txt", "w") as f:
            f.write(log + "\n")
        
async def find_full_lobby():
    '''Finds a full lobby and starts a game.'''
    while True:
        for lobby_id, lobby_data in LOBBYS.items():
            if "players" in lobby_data and lobby_id in players.keys():
                if len(lobby_data["players"]) == len(players[lobby_id]):
                    print("Full lobby found.")
                    await game(players[lobby_id], fields[lobby_id], lobby_id)
        await asyncio.sleep(5)

async def game(socket_list, field, lobby_id):
    '''Runs the game loop.'''
    score = {"red": 0, "blue": 0}
    
    log_game_moves("Game started.", lobby_id)
    # send field to all players
    playing_team = random.choice(socket_list).team
    waiting_team = "red" if playing_team == "blue" else "blue"
    print("playing team:", playing_team)
    
    while True:
        playing_team, waiting_team = waiting_team, playing_team
        await send_data_toall(socket_list, field)
        log_game_moves(f"Playing team: {playing_team}", lobby_id)
        log_game_moves(str(field), lobby_id)
        data = None
        
        for player in socket_list:
            if player.team == playing_team and isinstance(player, SpyMaster):
                log_game_moves(f"{player.name}'s turn to send .", lobby_id)
                await player.send_data("your turn")
                data = await player.recieve_data() # waiting for json {"hint": "test", "num_guesses": 2}
            else: 
                await player.send_data("turn : " + playing_team)
        
        #send hint to all players
        await send_data_toall(socket_list, data)

        log_game_moves(f"Hint: {data['hint']}, {data['num_guesses']}", lobby_id) # type: ignore
        
        for player in socket_list:
            if player.team == playing_team and isinstance(player, Agent):
                await player.send_data("send guess cards")
                if data is not None and "num_guesses" in data:
                    for i in range(data["num_guesses"]):
                        data = await player.recieve_data()  # waiting for json {"x": 0, "y": 0}
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
                        else:
                            break
                        await send_data_toall(socket_list, field)
        
        log_game_moves(f"Score: {score}", lobby_id)
        await send_data_toall(socket_list, score)
        print("score:", score)
        if (score["red"] == field.num_colored or score["blue"] == field.num_colored): 
            print("Game over.")
            break
        
    # end game
    for player in socket_list:
        await player.send_data("game over")
        player.socket.close()
        
    log_game_moves("Game over.", lobby_id)

async def handler(websocket, lobby):
    '''Handles connections to the server.'''
    await websocket.send("Hello from the server!")

    lobby_containing_player = lobby.players
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
    if not players.get(lobby_id_containing_player):
        if data["role"] == "spymaster": players[lobby_id_containing_player] = [SpyMaster(data["name"], data["team"], websocket)]
        elif data["role"] == "agent": players[lobby_id_containing_player] = [Agent(data["name"], data["team"], websocket)]
    else:
        if data["role"] == "spymaster": players[lobby_id_containing_player].append(SpyMaster(data["name"], data["team"], websocket))
        elif data["role"] == "agent": players[lobby_id_containing_player].append(Agent(data["name"], data["team"], websocket))
    
    connected_players = len(players[lobby_id_containing_player])

    # wait for everyone to connect
    log_game_moves(f"{data['name']} connected.", lobby_id_containing_player)
    await websocket.send("Waiting for everyone to connect...")
    while connected_players < len(lobby_containing_player["players"]):
        await asyncio.sleep(3)
        connected_players = len(players[lobby_id_containing_player])
    
    if connected_players == len(lobby_containing_player["players"]):
        if not fields.get(lobby_id_containing_player):
            fields[lobby_id_containing_player] = Field()
            
    try:
        await websocket.wait_closed()
    finally:
        print("Connection closed.")
        # remove player from socket list

app = FastAPI()

LOBBIES = {}


@app.websocket("/lobby/{lobby_id}")
async def lobby_endpoint(
    lobby_id: str,
    ws: WebSocket,
    user_id: Annotated[str | None, Header()] = Header(None),
    Authorization: Annotated[str | None, Header()] = Header(None),
    ):


    if user_id is None:
        await ws.send_text(str({"msg": "User ID is required."}))
        await ws.close()
        return
    
    if Authorization is None:
        await ws.send_text(str({"msg": "Authorization is required."}))
        await ws.close()
        return
    

    if lobby_id not in LOBBIES.keys():
        lobby_data = lobby_service.get_lobby_data(lobby_id)
        if lobby_data is None:
            ws.send_text(str({"msg": "Lobby not found."}))
            await ws.close()
            return
        lobby = Lobby(lobby_data["players"])
        lobby.set_host(lobby_data["host"])
        LOBBIES[lobby_id] = lobby
    if lobby_id in LOBBIES.keys():
        if lobby.status == "closed":
            lobby_data = lobby_service.get_lobby_data(lobby_id)
            if lobby_data is None:
                ws.send_text(str({"msg": "Lobby not found."}))
                await ws.close()
                return
            lobby = Lobby(lobby_data["players"])
            lobby.set_host(lobby_data["host"])
            LOBBIES[lobby_id] = lobby
        else:
            lobby = LOBBIES[lobby_id]
            lobby.add_player(ws)


    player = Player(user_id, Authorization, ws)

    await ws.accept()
    lobby.add_player(player)

    try:
        while True:
            # Wait for messages (in case you want to add more functionality)
            data = await ws.receive_text()
            handler(data, lobby)
    except Exception as e:
        print(e)
    finally:
        # Remove the player when the WebSocket connection is closed
        lobby.remove_player(user_id)
        if ws == lobby.host:
            lobby.close()
        await ws.close()

# async def main():
#     async with websockets.serve(handler, "localhost", 8081):
#         await find_full_lobby()

# if __name__ == "__main__":
#     asyncio.run(main())