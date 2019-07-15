from .board_test_helper import BoardTestHelper
from checkers.game import Game


class GameTestHelper(Game):
	def __init__(self, width=4, height=8, rows_per_user_with_pieces=3):
		Game.__init__(self, width, height, rows_per_user_with_pieces)
		self.board = BoardTestHelper(width, height, rows_per_user_with_pieces)
