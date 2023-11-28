from abc import ABC, abstractmethod
import asyncio
import json

import websockets

class Player():
  def __init__(self, name, team, socket) -> None:
    self._name = name
    self._team = team
    self._socket = socket
    
  @property
  def name(self):
    return self._name
  
  @property
  def team(self):
    return self._team
  
  @property
  def socket(self):
    return self._socket

  async def recieve_data(self, delay=1):
    await asyncio.sleep(delay)
    data = await self._socket.recv()
    return json.loads(data)

  async def send_data(self, data):
    if self._socket.open:
      print(f"Sending data to {self.name}")
      await self._socket.send(json.dumps(data))
    else:
      print("Socket closed for player", self.name)
      return "Socket closed."
    
  @abstractmethod  
  async def send_field(self, field):
    pass

  def __str__(self) -> str:
    return f"Player({self.name}, {self.team}, {self.socket})"
class SpyMaster(Player):
  def __init__(self, name, team, socket) -> None:
    super().__init__(name, team, socket)
  
  async def send_data(self, data):
    await super().send_data(data)
    
  async def recieve_data(self):
    return await super().recieve_data()

  async def send_field(self, field):
    await self.send_data(field.revealed())

class Agent(Player):
  def __init__(self, name, team, socket) -> None:
    super().__init__(name, team, socket)
    
  async def send_field(self, field):
    await self.send_data(field.hidden())

  async def send_data(self, data):
    await super().send_data(data)
    
  async def recieve_data(self):
    return await super().recieve_data()