from copy import deepcopy
from functools import reduce
import numpy as np
from .board_searcher import BoardSearcher
from .board_initializer import BoardInitializer

class Board:

	def __init__(self, width=4, height=8, rows_per_user_with_pieces=3):
		self.player_turn = 1
		self.width = width
		self.height = height
		self.position_count = self.width * self.height
		self.rows_per_user_with_pieces = rows_per_user_with_pieces
		self.position_layout = {}
		self.position_layout_2d = [[]]
		self.piece_requiring_further_capture_moves = None
		self.previous_move_was_capture = False
		self.searcher = BoardSearcher()
		self._possible_moves = None
		self._possible_capture_moves = None
		self._possible_positional_moves = None
		BoardInitializer(self).initialize()

	# Overriding this so that deepcopy doesn't include cached_values when copying
	def __deepcopy__(self, memo):
		copy = Board(width=self.width, height=self.height, rows_per_user_with_pieces=self.rows_per_user_with_pieces)
		copy.player_turn = self.player_turn
		copy.position_layout = deepcopy(self.position_layout)
		copy.position_layout_2d = deepcopy(self.position_layout_2d)
		copy.piece_requiring_further_capture_moves = self.piece_requiring_further_capture_moves
		copy.previous_move_was_capture = self.previous_move_was_capture
		copy.searcher = BoardSearcher()

		pieces = deepcopy(self.pieces)
		for piece in pieces:
			piece.board = copy
		copy.pieces = pieces

		# We don't want to copy these cached values
		copy._possible_moves = None
		copy._possible_capture_moves = None
		copy._possible_positional_moves = None

		return copy


	def count_movable_player_pieces(self, player_number = 1):
		return reduce((lambda count, piece: count + (1 if piece.is_movable() else 0)), self.searcher.get_pieces_by_player(player_number), 0)

	def get_uncaptured_pieces(self):
		return list(filter(lambda piece: piece.captured == False, self.pieces))

	def get_player_pieces(self, player_number):
		return self.searcher.get_pieces_by_player(player_number)

	def get_possible_moves(self):
		if self._possible_moves is None:
			capture_moves = self.get_possible_capture_moves()
			self._possible_moves = capture_moves if capture_moves else self.get_possible_positional_moves()
		return self._possible_moves

	def get_possible_capture_moves(self):
		if self._possible_capture_moves is None:
			pieces_that_can_capture = self.searcher.get_pieces_in_play()
			self._possible_capture_moves = self._get_possible_capture_moves_for_pieces(pieces_that_can_capture)
		return self._possible_capture_moves

	def get_possible_capture_moves_for_last_capturer(self, last_capturer_position):
		return self._get_possible_capture_moves_for_pieces([self.searcher.get_piece_by_position(last_capturer_position)])

	def _get_possible_capture_moves_for_pieces(self, pieces_that_can_capture):
		return reduce((lambda moves, piece: moves + piece.get_possible_capture_moves()), pieces_that_can_capture, [])

	def get_possible_positional_moves(self):
		if self._possible_positional_moves is None:
			self._possible_positional_moves = reduce((lambda moves, piece: moves + piece.get_possible_positional_moves()), self.searcher.get_pieces_in_play(), [])
		return self._possible_positional_moves

	def position_is_open(self, position):
		return not self.searcher.get_piece_by_position(position)

	def move(self, move):
		if move in self.get_possible_capture_moves():
			self.perform_capture_move(move)
		else:
			self.perform_positional_move(move)

		return self

	def perform_capture_move(self, move):
		self.previous_move_was_capture = True
		piece = self.searcher.get_piece_by_position(move[0])
		originally_was_king = piece.king
		enemy_piece = piece.get_capture_move_enemy(move[1])
		enemy_piece.capture()
		self.move_piece(move, True)
		further_capture_moves_for_piece = [capture_move for capture_move in self.get_possible_capture_moves_for_last_capturer(move[1]) if capture_move[0] == move[1]]

		if further_capture_moves_for_piece and (originally_was_king == piece.king):
			self.piece_requiring_further_capture_moves = self.searcher.get_piece_by_position(move[1])
		else:
			self.piece_requiring_further_capture_moves = None
			self.switch_turn()

	def perform_positional_move(self, move):
		self.previous_move_was_capture = False
		self.move_piece(move, False)
		self.switch_turn()

	def switch_turn(self):
		self.player_turn = 1 if self.player_turn == 2 else 2

	def move_piece(self, move, is_capture):
		self.searcher.get_piece_by_position(move[0]).move(move[1])

		# clear cached values
		self._possible_moves = None
		self._possible_capture_moves = None
		self._possible_positional_moves = None

		self.pieces = sorted(self.pieces, key = lambda piece: piece.position if piece.position else 0)

	def is_valid_row_and_column(self, row, column):
		if row < 0 or row >= self.height:
			return False

		if column < 0 or column >= self.width:
			return False

		return True

	def __setattr__(self, name, value):
		super(Board, self).__setattr__(name, value)

		if name == 'pieces':
			[piece.reset_for_new_board() for piece in self.pieces]

			self.searcher.build(self)

	@classmethod
	def flip_2d(cls, position_layout_2d):
		'''
		Flip the entire board 180 degrees, leaving the pieces in their relative positions.  
		For example, flipping a the board for a new game would put the white pieces in 
		positions 1-12 and the black pieces in positions 25-36.  This will help with 
		training the model so that you can use each board position from the viewpoint 
		of the player.  

		Arguments:
		position_layout_2d - a 2D array
		'''
		return np.flip(np.array(position_layout_2d))

	def flip_position(self, position):
		'''
		Flip the entire board 180 degrees, leaving the pieces in their relative positions.  
		For example, flipping a the board for a new game would put the white pieces in 
		positions 1-12 and the black pieces in positions 25-36.  This will help with 
		training the model so that you can use each board position from the viewpoint 
		of the player.  

		Arguments:
		position - an integer board position on a standard board (with black on top)
		'''
		row, col = np.argwhere(self.position_layout_2d == position)[0]
		flipped_board = Board.flip_2d(self.position_layout_2d)
		return flipped_board[row][col]