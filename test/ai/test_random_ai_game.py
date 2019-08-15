import unittest
from ai.games.random_ai_game import RandomAIGame

class TestRandomAIGame(unittest.TestCase):
    def test_random_game(self):
        game = RandomAIGame()
        game.play()