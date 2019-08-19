from copy import deepcopy
from .board import Board

class Game:
	CONSECUTIVE_NONCAPTURE_MOVE_LIMIT = 40
	
	def __init__(self, width=4, height=8, rows_per_user_with_pieces=3, board=None):
		self.board = board or Board(width, height, rows_per_user_with_pieces)
		self.moves = []
		self.moves_since_last_capture = 0
		self.previous_state = None

	# Overriding this so that deepcopy doesn't include previous_state when copying
	def __deepcopy__(self, memo):
		board = deepcopy(self.board, memo)
		copy = Game(board=board)
		copy.moves = deepcopy(self.moves, memo)
		copy.moves_since_last_capture = self.moves_since_last_capture
		return copy

	def move(self, move):
		if move not in self.get_possible_moves():
			raise ValueError('The provided move is not possible')

		copy = deepcopy(self)
		copy.previous_state = self

		copy.board.move(move)
		copy.moves.append(move)
		copy.moves_since_last_capture = 0 if copy.board.previous_move_was_capture else copy.moves_since_last_capture + 1

		return copy

	def move_limit_reached(self):
		return self.moves_since_last_capture >= Game.CONSECUTIVE_NONCAPTURE_MOVE_LIMIT

	def is_over(self):
		return self.move_limit_reached() or not self.get_possible_moves()

	def get_winner(self):
		if self.is_over():
			if self.move_limit_reached():
				return None
			elif not self.board.count_movable_player_pieces(1):
				return 2
			elif not self.board.count_movable_player_pieces(2):
				return 1
		return None

	def black_wins(self):
		return self.is_over() and self.get_winner() == 1

	def white_wins(self):
		return self.is_over() and self.get_winner() == 2

	def is_draw(self):
		return self.is_over() and self.get_winner() is None

	def get_uncaptured_pieces(self):
		return self.board.get_uncaptured_pieces()

	def get_possible_moves(self):
		return self.board.get_possible_moves()

	def whose_turn(self):
		return self.board.player_turn

	def get_position_layout_2d(self, flip_for_white=False):
		return Board.flip_2d(self.board.position_layout_2d) if (flip_for_white and self.whose_turn() == 2) else self.board.position_layout_2d

	def get_game_states(self):
		return [*(self.previous_state.get_game_states() if self.previous_state is not None else []), self]

