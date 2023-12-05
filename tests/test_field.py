import sys
import os
current_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_script_dir, '../'))

import unittest
from classes.field import Field
from classes.card import Card

class TestField(unittest.TestCase):
    def setUp(self):
        self.field = Field()

    def test_num_colored(self):
        self.assertEqual(self.field.num_colored, 3)

    def test_generate_words(self):
        words = self.field.generate_words(16)
        self.assertEqual(len(words), 16)

    def test_generate_field(self):
        field = self.field.generate_field(6)
        self.assertEqual(len(field), self.field._height)
        self.assertEqual(len(field[0]), self.field._width)

    def test_hidden(self):
        hidden = self.field.hidden()
        self.assertEqual(len(hidden), self.field._height)
        self.assertEqual(len(hidden[0]), self.field._width)

    def test_revealed(self):
        revealed = self.field.revealed()
        self.assertEqual(len(revealed), self.field._height)
        self.assertEqual(len(revealed[0]), self.field._width)

    def test_toggle_revealed(self):
        self.field.toggle_revealed(0, 0)
        card = self.field.get_card(0, 0)
        self.assertTrue(card.revealed)

    def test_get_card(self):
        card = self.field.get_card(0, 0)
        self.assertIsInstance(card, Card)

    def test_str(self):
        field_str = str(self.field)
        self.assertIsInstance(field_str, str)
        
if __name__ == "__main__":
    unittest.main()