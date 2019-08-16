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
		BoardInitializer(self).initialize()

	def count_movable_player_pieces(self, player_number = 1):
		return reduce((lambda count, piece: count + (1 if piece.is_movable() else 0)), self.searcher.get_pieces_by_player(player_number), 0)

	def get_uncaptured_pieces(self):
		return list(filter(lambda piece: piece.captured == False, self.pieces))

	def get_player_pieces(self, player_number):
		return self.searcher.get_pieces_by_player(player_number)

	def get_possible_moves(self):
		capture_moves = self.get_possible_capture_moves()

		return capture_moves if capture_moves else self.get_possible_positional_moves()

	def get_possible_capture_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_capture_moves()), self.searcher.get_pieces_in_play(), [])

	def get_possible_positional_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_positional_moves()), self.searcher.get_pieces_in_play(), [])

	def position_is_open(self, position):
		return not self.searcher.get_piece_by_position(position)

	def create_new_board_from_move(self, move):
		new_board = deepcopy(self)

		if move in self.get_possible_capture_moves():
			new_board.perform_capture_move(move)
		else:
			new_board.perform_positional_move(move)

		return new_board

	def perform_capture_move(self, move):
		self.previous_move_was_capture = True
		piece = self.searcher.get_piece_by_position(move[0])
		originally_was_king = piece.king
		enemy_piece = piece.capture_move_enemies[move[1]]
		enemy_piece.capture()
		self.move_piece(move)
		further_capture_moves_for_piece = [capture_move for capture_move in self.get_possible_capture_moves() if move[1] == capture_move[0]]

		if further_capture_moves_for_piece and (originally_was_king == piece.king):
			self.piece_requiring_further_capture_moves = self.searcher.get_piece_by_position(move[1])
		else:
			self.piece_requiring_further_capture_moves = None
			self.switch_turn()

	def perform_positional_move(self, move):
		self.previous_move_was_capture = False
		self.move_piece(move)
		self.switch_turn()

	def switch_turn(self):
		self.player_turn = 1 if self.player_turn == 2 else 2

	def move_piece(self, move):
		self.searcher.get_piece_by_position(move[0]).move(move[1])
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
		flipped_board = np.flip(self.position_layout_2d)
		return flipped_board[row][col]