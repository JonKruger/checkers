import unittest
from ai.games.ai_game import AIGame
from ai.players.random_ai_player import RandomAIPlayer
from ai.players.nn_player import NNPlayer
from ai.analyzer.nn_trainer import NNTrainer

class TestNNTrainerGame(unittest.TestCase):
    def test_game_with_nn_player(self):
        game = AIGame(RandomAIPlayer(), NNPlayer(NNTrainer().get_model()))
        game.play()