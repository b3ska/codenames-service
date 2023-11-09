from abc import ABC, abstractmethod

class Player(ABC):
  def __init__(self, name, team) -> None:
    self._name = name
    self._team = team

  @abstractmethod
  def get_clue(self, clue):
    pass

  @abstractmethod
  def post_clue(self, clue):
    pass


class SpyMaster(Player):
  def __init__(self, name, team) -> None:
    super().__init__(name, team)
  
  def post_clue(self, clue):
    print(f"SpyMaster {self._name} posted clue: {clue}")

class Agent(Player):
  def __init__(self, name, team) -> None:
    super().__init__(name, team)

  def get_clue(self, clue):
    print(f"Agent {self._name} received clue: {clue}")