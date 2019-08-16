from copy import deepcopy
from .board import Board

class Game:
	CONSECUTIVE_NONCAPTURE_MOVE_LIMIT = 40
	
	def __init__(self, width=4, height=8, rows_per_user_with_pieces=3):
		self.board = Board(width, height, rows_per_user_with_pieces)
		self.moves = []
		self.moves_since_last_capture = 0

	def copy(self):
		copy = Game()
		copy.board = self.board.copy()
		copy.moves = self.moves.copy()
		copy.moves_since_last_capture = self.moves_since_last_capture
		return copy

	def move(self, move):
		if move not in self.get_possible_moves():
			raise ValueError('The provided move is not possible')

		copy = deepcopy(self)

		copy.board.move(move)
		copy.moves.append(move)
		copy.moves_since_last_capture = 0 if copy.board.previous_move_was_capture else copy.moves_since_last_capture + 1

		return copy

	def move_limit_reached(self):
		return self.moves_since_last_capture >= Game.CONSECUTIVE_NONCAPTURE_MOVE_LIMIT

	def is_over(self):
		return self.move_limit_reached() or not self.get_possible_moves()

	def get_winner(self):
		if not self.board.count_movable_player_pieces(1):
			return 2
		elif not self.board.count_movable_player_pieces(2):
			return 1
		else:
			return None

	def get_uncaptured_pieces(self):
		return self.board.get_uncaptured_pieces()

	def get_possible_moves(self):
		return self.board.get_possible_moves()

	def whose_turn(self):
		return self.board.player_turn