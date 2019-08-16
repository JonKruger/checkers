import unittest
from ai.analyzer.weighted_win_likelihood_analyzer import WeightedWinLikelihoodAnalyzer
from ai.games.random_ai_game import RandomAIGame

class TestWeightedWinLikelihoodAnalyzer(unittest.TestCase):
    def test_analyzer(self):
        game = RandomAIGame()
        moves, winner = game.play()

        WeightedWinLikelihoodAnalyzer().analyze_game(moves)