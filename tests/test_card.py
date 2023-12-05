import sys
import os
current_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_script_dir, '../'))

import unittest
from classes.card import Card

class TestCard(unittest.TestCase):
    def test_card_initialization(self):
        card = Card(color="red", value="A")
        self.assertEqual(card.color, "red")
        self.assertEqual(card.value, "A")
        self.assertFalse(card._revealed)
        
    def test_card_flip(self):
        card = Card(color="blue", value="B")
        self.assertFalse(card._revealed)
        card.flip()
        self.assertTrue(card._revealed)
        card.flip()
        self.assertTrue(card._revealed)
        
    def test_card_string_representation(self):
        card = Card(color="green", value="C")
        card.flip()
        self.assertEqual(str(card), "Card(green, C)")

if __name__ == '__main__':
    unittest.main()