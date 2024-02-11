# main file for codenames-service, runs the server and handles connections,
# also handles the game logic, and the game log.
from fastapi import FastAPI, WebSocket, Header
from typing import Annotated
import asyncio
import random
import json
from classes.lobby import Lobby
from classes.card import Card
from classes.player import SpyMaster, Player
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

async def handler(msg, lobby, uid, ws):
    try:
        message = json.loads(msg)
        print(message)
        msg_type = message.get("type")
    except Exception as e:
        print(f"Error parsing message from player {str(msg)}")

    event_handlers = {
        "move": lobby.handle_move,
        "info": lobby.info_handler,
        "game_state": lobby.handle_game_state
        # Add more event handlers as needed
    }

    # Call the appropriate event handler based on the message type
    event_handler = event_handlers.get(msg_type)
    if event_handler:
        try:
            await event_handler(message, uid)
        except Exception as e:
            print(f"Error processing message from player {uid}: {str(e)}")
    print(message)

app = FastAPI()

LOBBIES = {}


@app.websocket("/lobby/{lobby_id}")
async def lobby_endpoint(
    lobby_id: str,
    ws: WebSocket,
    user_id: str | None = Header(default=None),
    Authorization: str | None = Header(default=None),
    ):


    if user_id is None:
        await ws.send_text(str({"type": "info", "msg": "User ID is required."}))
        await ws.close()
        return
    
    if Authorization is None:
        await ws.send_text(str({"type": "info", "msg": "Authorization is required."}))
        await ws.close()
        return
    

    if lobby_id not in LOBBIES.keys():
        lobby_data = lobby_service.get_lobby_data(lobby_id)
        if lobby_data is None:
            ws.send_text(str({"type": "info", "msg": "Lobby not found."}))
            await ws.close()
            return
        lobby = Lobby(lobby_data["players"])
        lobby.set_host(lobby_data["host"])
        LOBBIES[lobby_id] = lobby
    if lobby_id in LOBBIES.keys():
        if lobby.status == "closed":
            lobby_data = lobby_service.get_lobby_data(lobby_id)
            if lobby_data is None:
                ws.send_text(str({"type": "info", "msg": "Lobby not found."}))
                await ws.close()
                return
            lobby = Lobby(lobby_data["players"])
            lobby.set_host(lobby_data["host"])
            LOBBIES[lobby_id] = lobby
        else:
            lobby = LOBBIES[lobby_id]
            lobby.add_player(ws)


    player = Player(user_id, Authorization, ws, "red", "SpyMaster")

    await ws.accept()
    lobby.add_player(player)

    try:
        while True:
            # Wait for messages (in case you want to add more functionality)
            data = await ws.receive_text()
            handler(data, lobby, player.uid, ws)
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