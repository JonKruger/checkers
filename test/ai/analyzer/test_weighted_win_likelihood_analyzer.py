import unittest
from test.test_helpers.game_test_helper import GameTestHelper
import numpy as np
from ai.analyzer.weighted_win_likelihood_analyzer import WeightedWinLikelihoodAnalyzer, State
from ai.analyzer.nn_trainer import NNTrainer
from ai.games.random_ai_game import RandomAIGame

class TestWeightedWinLikelihoodAnalyzer(unittest.TestCase):
    def test_analyzer(self):
        game = RandomAIGame()
        game.play()

#        weights = WeightedWinLikelihoodAnalyzer().analyze_game(game.current_state())
#        NNTrainer().train(weights)

    def test_get_board_position_2d_black(self):
        game = GameTestHelper()
        game.board.set_pieces(['B 5','W 6','B king 4', 'W king 32'], 1)

        board_position_2d = State(game).get_board_position_2d(1)
        np.testing.assert_array_equal(board_position_2d, [[0,0,0,3],[1,-1,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,-3]])

    def test_get_board_position_2d_white(self):
        game = GameTestHelper()
        game.board.set_pieces(['B 5','W 6','B king 4', 'W king 32'], 2)

        board_position_2d = State(game).get_board_position_2d(2)
        print(board_position_2d)
        np.testing.assert_array_equal(board_position_2d, [[3,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,1,-1],[-3,0,0,0]])
