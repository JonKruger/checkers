import numpy as np
from checkers.game import Game
from checkers.board import Board

class BoardPosition:
    def __init__(self, whose_turn, uncaptured_pieces, possible_moves, winner, previous_board_position):
        self.whose_turn = whose_turn
        self.uncaptured_pieces = uncaptured_pieces
        self.possible_moves = possible_moves
        self.winner = winner
        self.previous_board_position = previous_board_position
        self.next_board_position = None
        self.black_weighted_board_position = None
        self.white_weighted_board_position = None

    def __str__(self):
        black_pieces = len(list(filter(lambda p: p.player == 1 and p.king == False, self.uncaptured_pieces)))
        black_kings = len(list(filter(lambda p: p.player == 1 and p.king == True, self.uncaptured_pieces)))
        white_pieces = len(list(filter(lambda p: p.player == 2 and p.king == False, self.uncaptured_pieces)))
        white_kings = len(list(filter(lambda p: p.player == 2 and p.king == True, self.uncaptured_pieces)))
        return f'{"Black" if self.whose_turn == 1 else "White"} turn, {black_pieces} B/{black_kings} BK/{white_pieces} W/{white_kings} WK, {len(self.possible_moves)} possible moves, winner is {self.winner}'

class WeightedBoardPosition:
    def __init__(self, board_position_2d, weight):
        assert type(board_position_2d) == np.ndarray
        assert len(board_position_2d.shape) == 2
        assert type(weight) == float
        assert 0 <= weight <= 1

        self.board_position_2d = board_position_2d
        self.weight = weight

class WeightedWinLikelihoodAnalyzer:
    def analyze_game(self, moves):
        # Replay the game, taking note of the board after each move
        # Work backwards - for each board position, what are the possible moves, and what is the likelihood of a win in that position?
        black_board_positions = []
        white_board_positions = []

        board_positions, board = self._get_board_positions(moves)
        print(f'I found {len(board_positions)} positions')
        weights = self._calculate_weights(board_positions, board)
        
    def _get_board_positions(self, moves):
        board_positions = []
        game = Game()

        # starting board position
        whose_turn, uncaptured_pieces, possible_moves, winner = game.whose_turn(), game.get_uncaptured_pieces(), game.get_possible_moves(), game.get_winner()
        board_position = BoardPosition(whose_turn, uncaptured_pieces, possible_moves, winner, None)
        previous_board_position = board_position

        for move in moves:
            game = game.move(move)
            whose_turn, uncaptured_pieces, possible_moves, winner = game.whose_turn(), game.get_uncaptured_pieces(), game.get_possible_moves(), game.get_winner()
            board_position = BoardPosition(whose_turn, uncaptured_pieces, possible_moves, winner, previous_board_position)
            previous_board_position.next_board_position = board_position
            board_positions.append(board_position)
            previous_board_position = board_position
        return board_positions, game.board

    def _calculate_weights(self, board_positions, board):
        for board_position in reversed(board_positions):
            weight, inverse_weight = None, None
            board_position_2d = self._get_board_position_2d(board_position.uncaptured_pieces, board, board_position.whose_turn)
            if (board_position.winner is not None):
                # The game ended
                # TODO: handle draws
                weight = 1. if board_position.winner == board_position.whose_turn else 0.
                inverse_weight = 1. - weight
            else:
                pass


    def _get_board_position_2d(self, uncaptured_pieces, board, player_number):
        result = np.tile(0, [board.height, board.width])

        for piece in uncaptured_pieces:
            x = int((piece.position - 1) / board.width)
            y = int((piece.position - 1) % board.width)
            value = (3 if piece.king else 1) * (1 if piece.player == player_number else -1)
            result[x,y] = value

        if player_number == 2:
            result = Board.flip_2d(result)
        return result


    
