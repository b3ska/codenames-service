import numpy as np
import random
from classes import Card

class Field:
    def __init__(self, width=4, height=4, num_colored=6, num_black=1, num_white=1) -> None:
        self._width = width
        self._height = height
        self._num_colored = num_colored
        self._num_black = num_black
        self._num_white = num_white
        self._field = self.generate_field()
        
    @property
    def num_colored(self):
        return self._num_colored

    def generate_words(self, num_words):
        words = []
        f = open('./codenames-service/classes/values.txt', 'r')
        for word in f.read().split(','):
            words.append(word)
        random.shuffle(words)
        return words[:num_words]

    def generate_field(self):
        field = []
        words = self.generate_words(self._width * self._height)
        for i in range(self._height):
            field.append([])
            for j in range(self._width):
                if self._num_colored > 0:
                    self._num_colored -= 1
                    color = "red" if self._num_colored % 2 else "blue"
                elif self._num_black > 0:
                    self._num_black -= 1
                    color = "black"
                elif self._num_white > 0:
                    self._num_white -= 1
                    color = "white"
                else:
                    color = "gray"
                field[i].append(Card.Card(color, words.pop()))     
        np.random.shuffle(field)
        return field
    
    def hidden(self):
        return [[card.hidden for card in row] for row in self._field]
    
    def revealed(self):
        return [[card.revealed for card in row] for row in self._field]
    
    def toggle_revealed(self, x, y):
        self._field[x][y].flip()
    
    def get_card(self, x, y):
        return self._field[x][y]
    
    def __str__(self) -> str:
        field = "FIELD:\n"
        for row in self._field:
            for card in row:
                field += str(card) + "\t"
            field += "\n"
        return field