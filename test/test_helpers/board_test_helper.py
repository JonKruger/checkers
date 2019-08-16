from checkers.board import Board
from checkers.piece import Piece

class BoardTestHelper(Board):
    def __init__(self, width=4, height=8, rows_per_user_with_pieces=3):
        Board.__init__(self, width, height, rows_per_user_with_pieces)

    def set_pieces(self, pieces, whose_turn):
        pieces = [BoardTestHelper.parse_piece_notation(p) for p in pieces]
        for piece in pieces:
            piece.board = self
        self.pieces = pieces
        self.player_turn = whose_turn

    def parse_piece_notation(notation):
        values = notation.split() 
        
        piece = Piece()
        
        if values[0] == 'B':
            piece.player = 1
        elif values[0] == 'W':
            piece.player = 2
        else:
            raise Exception('Invalid player notation, should be "B" or "W"')

        piece.king = (values[1] == 'king')
        piece.position = int(values[-1])
        return piece
