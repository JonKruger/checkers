from copy import deepcopy
from .board import Board

class Game:
	CONSECUTIVE_NONCAPTURE_MOVE_LIMIT = 40
	
	def __init__(self, width=4, height=8, rows_per_user_with_pieces=3, board=None):
		self.board = board or Board(width, height, rows_per_user_with_pieces)
		self.moves = []
		self.moves_since_last_capture = 0
		self.previous_state = None
		self._possible_next_states = None

	# Overriding this so that deepcopy doesn't include previous_state when copying
	def __deepcopy__(self, memo):
		board = deepcopy(self.board, memo)
		copy = Game(board=board)
		copy.moves = deepcopy(self.moves, memo)
		copy.moves_since_last_capture = self.moves_since_last_capture

		# Don't copy cached values
		copy.previous_state = None
		copy._possible_next_states = None

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

	def get_possible_next_states(self, actual_next_state=None, force_reload=False):
		# If we have a cached list of next states and someone passes in an actual_next_state
		# that isn't in that list, we have to reload the list.
		if self._possible_next_states is not None and actual_next_state is not None and actual_next_state not in self._possible_next_states:
			force_reload = True

		if self._possible_next_states is None or force_reload == True:
			self._possible_next_states = []

			actual_next_move = None
			if actual_next_state is not None:
				actual_next_move = actual_next_state.last_move()

			for move in self.get_possible_moves():
				if move == actual_next_move:
					self._possible_next_states.append(actual_next_state)
				else:
					self._possible_next_states.append(self.move(move))

		return self._possible_next_states	

	def whose_turn(self):
		return self.board.player_turn

	def get_position_layout_2d(self, player):
		return Board.flip_2d(self.board.position_layout_2d) if player == 2 else self.board.position_layout_2d

	def get_game_states(self):
		return [*(self.previous_state.get_game_states() if self.previous_state is not None else []), self]

	def board_height(self):
		return self.board.height

	def board_width(self):
		return self.board.width

	def last_move(self):
		return self.moves[-1] if (len(self.moves) > 0) else None
