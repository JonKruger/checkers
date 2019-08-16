from checkers.game import Game

class BoardPosition:
    def __init__(self, whose_turn, uncaptured_pieces, possible_moves, terminal_result, previous_board_position):
        self.whose_turn = whose_turn
        self.uncaptured_pieces = uncaptured_pieces
        self.possible_moves = possible_moves
        self.terminal_result = terminal_result
        self.previous_board_position = previous_board_position

class WeightedWinLikelihoodAnalyzer:
    def analyze_game(moves):
        # Replay the game, taking note of the board after each move
        # Work backwards - for each board position, what are the possible moves, and what is the likelihood of a win in that position?
        black_board_positions = []
        white_board_positions = []
        
        game = Game()
        whose_turn, uncaptured_pieces, possible_moves, winner = game.whose_turn(), game.get_uncaptured_pieces(), game.get_possible_moves, game.get_winner()
        if (whose_turn)
