# Card class, used to represent a single card in the game.
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
  def hidden(self):
    return {"color" : self.color, "value" : self.value} if self._revealed else {"color" : None, "value" : self.value}
  
  @property
  def revealed(self):
    return {"color" : self.color, "value" : self.value}
  
  @color.setter
  def color(self, color):
    self._color = color
  
  @value.setter
  def value(self, value):
    self._value = value

  def flip(self) -> None:
    '''Flips the card over, revealing the color and value.'''
    if not self._revealed: self._revealed = not self._revealed
    else: return 

  def __str__(self) -> str:
    '''Returns a string representation of the card.'''
    return f"Card({self.color}, {self.value})"