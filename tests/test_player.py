
import sys
import os
import unittest

current_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_script_dir, '../'))

import unittest
from classes.field import Field
from classes.card import Card
from classes.player import SpyMaster
from classes.player import Agent
from classes.player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        # Create a sample player for testing
        self.player = Player("John", "Red", None)

    def test_name(self):
        self.assertEqual(self.player.name, "John")

    def test_team(self):
        self.assertEqual(self.player.team, "Red")

    def test_socket(self):
        self.assertIsNone(self.player.socket)

    def test_str(self):
        self.assertEqual(str(self.player), "Player(John, Red, None)")

if __name__ == "__main__":
    unittest.main()