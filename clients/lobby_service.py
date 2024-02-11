import requests


LOBBY_SERVICE = "http://127.0.0.1:8080"

def get_lobby_data(lobby_id: str):
    response = requests.get(f"{LOBBY_SERVICE}/api/v1/lobby/{lobby_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None 