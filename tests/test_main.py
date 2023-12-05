import sys
import os
current_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_script_dir, '../'))

import unittest
from unittest.mock import MagicMock, patch
from classes.field import Field
from classes.player import Player, SpyMaster, Agent
from main import game

class TestGame(unittest.TestCase):
    async def test_handler(self):
        pass
    
    async def test_game(self):
        pass
    
    async def test_send_data_toall(self):
        pass

if __name__ == "__main__":
    unittest.main()