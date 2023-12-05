# field generator, manipulator, and accessor
import numpy as np
import random
import json
from classes.card import Card

WORDS_FILE_PATH = json.load(open('config.json', 'r'))["filename_words"]

class Field:
    def __init__(self, width=4, height=4, num_colored=6, num_black=1, num_white=1) -> None:
        self._width = width
        self._height = height
        self._num_colored = num_colored // 2
        self._num_black = num_black
        self._num_white = num_white
        self._field = self.generate_field(num_colored)
        
    @property
    def num_colored(self):
        return self._num_colored

    def generate_words(self, num_words):
        '''Generates a list of words from the values.txt file.'''
        words = []
        f = open(WORDS_FILE_PATH, 'r')
        for word in f.read().split(','):
            words.append(word)
        random.shuffle(words)
        return words[:num_words]

    def generate_field(self, num_colored):
        '''Generates a field of cards, with the specified number of colored, black, and white cards.'''
        field = []
        words = self.generate_words(self._width * self._height)
        for i in range(self._height):
            field.append([])
            for j in range(self._width):
                if num_colored > 0:
                    num_colored -= 1
                    color = "red" if num_colored % 2 else "blue"
                elif self._num_black > 0:
                    self._num_black -= 1
                    color = "black"
                elif self._num_white > 0:
                    self._num_white -= 1
                    color = "white"
                else:
                    color = "gray"
                field[i].append(Card(color, words.pop()))     
        np.random.shuffle(field)
        return field
    
    def hidden(self):
        ''''Returns a list of lists of hidden cards.'''
        return list(map(lambda row: list(map(lambda card: card.hidden, row)), self._field))
    
    def revealed(self):
        '''Returns a list of lists of revealed cards.'''
        return list(map(lambda row: list(map(lambda card: card.revealed, row)), self._field))
    
    def toggle_revealed(self, x, y):
        '''Toggles the revealed state of the card at the specified coordinates.'''
        self._field[x][y].flip()
    
    def get_card(self, x, y):
        '''Returns the card at the specified coordinates.'''
        return self._field[x][y]
    
    def __str__(self) -> str:
        '''Returns a string representation of the field.'''
        field = "FIELD:\n"
        for row in self._field:
            for card in row:
                field += str(card) + "\t"
            field += "\n"
        return field