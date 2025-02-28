from abc import abstractmethod
import json
from fastapi import WebSocket
  
class Player:
    def __init__(self, uid: str, auth:str, ws: WebSocket, team: str, role: str):
      self._uid = uid
      self._wd = ws
      self._team = team
      self._role = role

    @property
    def name(self):
      return self._uid
    
    @property
    def _team(self):
      return self._team
    
    @property
    def socket(self):
      return self._socket

    def update_role(self, role: str):
      self._role = role

    def update_team(self, team: str):
      self._team = team

    async def send_msg(self, message: str):
        await self._wd.send_text(message)
    
    async def get_player_input(self) -> str:
        ret = await self.socket.receive_text()
        return ret
  
    def __str__(self) -> str:
      return f"Player({self._uid}, {self._team}, {self._role}, {self._wd})"



class SpyMaster(Player):
  def __init__(self, name, team, socket) -> None:
    super().__init__(name, team, socket)
  
  async def send_data(self, data):
    '''calls super().send_data(data)'''
    await super().send_data(data)
    
  async def recieve_data(self):
    '''calls super().recieve_data()'''
    return await super().recieve_data()

  async def send_field(self, field):
    '''Sends the revealed field to the player.'''
    await self.send_data(field.revealed())

class Agent(Player):
  def __init__(self, name, team, socket) -> None:
    super().__init__(name, team, socket)
    
  async def send_field(self, field):
    '''Sends the hidden field to the player.'''
    await self.send_data(field.hidden())

  async def send_data(self, data):
    '''calls super().send_data(data)'''
    await super().send_data(data)
    
  async def recieve_data(self):
    return await super().recieve_data()