import numpy as np
import random
from classes import Card

def generate_words(num_words):
    words = []
    f = open('values.txt', 'r')
    for word in f.read().split(','):
        words.append(word)
    random.shuffle(words)
    return words[:num_words]

def generate_field(width, height, num_colored=6, num_black=1, num_white=1):
    field = []
    words = generate_words(width * height)
    for i in range(height):
        field.append([])
        for j in range(width):
            if num_colored > 0:
                num_colored -= 1
                color = "red" if num_colored % 2 else "blue"
            elif num_black > 0:
                num_black -= 1
                color = "black"
            elif num_white > 0:
                num_white -= 1
                color = "white"
            else:
                color = "gray"
            field[i].append(Card.Card(color, words.pop()))
            
    np.random.shuffle(field)
    return field

field = generate_field(4, 4 )
for row in field:
    print("\n")
    for card in row:
        print(card.value, card.color, end="\t")