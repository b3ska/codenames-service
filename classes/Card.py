from abc import ABC, abstractmethod
from typing import Any
class Card():
  def __init__(self, color="gray", value="") -> None:
    self.color = color
    self.value = value
    self._revealed = False
  
  @property
  def color(self):
    return self._color
  
  @property
  def value(self):
    return self._value
  
  @property
  def revealed(self):
    return self._revealed
  
  @color.setter
  def color(self, color):
    self._color = color
  
  @value.setter
  def value(self, value):
    self._value = value

  def flip(self) -> None:
    if not self.revealed: self._revealed = not self._revealed
    else: return 

  def __str__(self) -> str:
    return f"Card({self.color}, {self.value})"