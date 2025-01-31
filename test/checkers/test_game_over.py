import unittest
from checkers.game import Game

import random

class TestGameOver(unittest.TestCase):

	def setUp(self):
		self.game = Game()

	def test_new_game_not_over(self):
		self.expect(False)

	def test_win_by_capture(self):
		self.make_non_final_moves([[10, 14], [23, 18], [14, 23], [26, 19], [11, 15], [19, 10], [6, 15], [22, 18], [15, 22], [25, 18], [9, 13], [21, 17], [13, 22],
			[31, 26], [22, 31], [24, 19], [31, 24], [24, 15], [15, 22], [29, 25], [22, 29], [30, 25], [29, 22], [28, 24], [12, 16], [32, 27], [16, 20], [27, 23],
			[20, 27], [23, 18]])

		self.move([22, 15]).expect(True)

	def test_win_by_no_legal_moves(self):
		self.make_non_final_moves([[11, 15], [22, 18], [15, 22], [25, 18], [12, 16], [18, 14], [9, 18], [23, 14], [10, 17], [21, 14], [5, 9], [14, 5], [6, 9],
			[29, 25], [9, 13], [25, 22], [2, 6], [22, 18], [13, 17], [27, 23], [17, 21], [24, 19], [8, 12], [30, 25], [21, 30], [28, 24], [4, 8], [18, 14], [6, 10],
			[32, 27], [10, 17], [23, 18], [16, 23], [23, 32], [24, 19], [30, 23], [23, 14], [31, 27], [32, 23]])

		self.move([23, 16]).expect(True)

	def test_move_limit_draw(self):
		self.make_non_final_moves([[10, 14], [22, 17], [9, 13], [17, 10], [7, 14], [25, 22], [6, 10], [29, 25], [1, 6], [22, 18], [6, 9], [24, 19], [2, 6], [28, 24],
			[11, 16], [24, 20], [8, 11], [32, 28], [4, 8], [27, 24], [3, 7], [31, 27], [13, 17], [25, 22], [9, 13], [18, 9], [9, 2], [10, 14], [22, 18], [5, 9], [19, 15],
			[16, 19], [23, 16], [12, 19], [30, 25], [14, 23], [23, 32], [21, 14], [14, 5], [11, 18], [2, 11], [11, 4], [19, 23], [26, 19], [13, 17], [25, 21], [17, 22],
			[21, 17], [22, 25], [17, 14], [18, 22], [5, 1], [22, 26], [4, 8], [26, 31], [19, 15], [25, 30], [8, 11], [31, 26], [1, 6], [26, 23], [24, 19], [23, 16],
			[16, 7], [14, 10], [7, 14], [15, 10], [14, 7], [28, 24], [32, 28], [20, 16], [28, 19], [19, 12], [6, 9], [7, 10], [9, 13], [10, 7], [13, 9], [7, 3], [9, 6],
			[3, 7], [6, 1], [7, 11], [1, 6], [11, 8], [6, 9], [8, 11], [9, 6], [11, 8], [6, 9], [8, 11], [9, 6], [11, 8], [6, 9], [8, 11], [9, 6], [11, 8], [6, 9], [8, 11],
			[9, 6], [11, 8], [6, 9], [8, 11], [9, 6], [11, 8], [6, 9], [8, 11], [9, 6], [11, 8], [6, 9], [8, 11], [9, 6]])

		self.move([11, 8]).expect(True)

	def test_resigning_current_player(self):
		game = Game()
		game = game.move([11,16])
		game = game.resign()
		self.assertTrue(game.is_over())
		self.assertEqual(game.get_winner(), 1)

	def test_resigning_player_1(self):
		game = Game()
		game = game.move([11,16])
		game = game.resign(resigning_player=1)
		self.assertTrue(game.is_over())
		self.assertEqual(game.get_winner(), 2)

	def test_resigning_player_2(self):
		game = Game()
		game = game.resign(resigning_player=2)
		self.assertTrue(game.is_over())
		self.assertEqual(game.get_winner(), 1)

	def test_agree_to_draw(self):
		game = Game()
		game = game.agree_to_draw()
		self.assertTrue(game.is_over())
		self.assertTrue(game.is_draw())

	def make_non_final_moves(self, moves):
		for move in moves:
			self.move(move).expect(False)

	def move(self, move):
		self.game = self.game.move(move)
		return self

	def expect(self, value):
		self.assertIs(self.game.is_over(), value)