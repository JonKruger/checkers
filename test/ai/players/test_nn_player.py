from ai.players.nn_player import NNPlayer
from checkers.game import Game
import unittest

class TestNNPlayer(unittest.TestCase):
    def test_predict(self):
        player = NNPlayer(1)
        game = Game()
        player.select_move(game, game.get_possible_moves())