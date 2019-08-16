from checkers.game import Game

class BoardPosition:
    def __init__(self, whose_turn, uncaptured_pieces, possible_moves, winner, previous_board_position):
        self.whose_turn = whose_turn
        self.uncaptured_pieces = uncaptured_pieces
        self.possible_moves = possible_moves
        self.winner = winner
        self.previous_board_position = previous_board_position

    def __str__(self):
        black_pieces = len(list(filter(lambda p: p.player == 1 and p.king == False, self.uncaptured_pieces)))
        black_kings = len(list(filter(lambda p: p.player == 1 and p.king == True, self.uncaptured_pieces)))
        white_pieces = len(list(filter(lambda p: p.player == 2 and p.king == False, self.uncaptured_pieces)))
        white_kings = len(list(filter(lambda p: p.player == 2 and p.king == True, self.uncaptured_pieces)))
        return f'{"Black" if self.whose_turn == 1 else "White"} turn, {black_pieces} B/{black_kings} BK/{white_pieces} W/{white_kings} WK, {len(self.possible_moves)} possible moves, winner is {self.winner}'

class WeightedWinLikelihoodAnalyzer:
    def analyze_game(self, moves):
        # Replay the game, taking note of the board after each move
        # Work backwards - for each board position, what are the possible moves, and what is the likelihood of a win in that position?
        black_board_positions = []
        white_board_positions = []

        board_positions = self._get_board_positions(moves)
        print(f'I found {len(board_positions)} positions')
        
    def _get_board_positions(self, moves):
        board_positions = []
        previous_board_position = None
        game = Game()

        for move in moves:
            print(move)
            game.move(move)
            whose_turn, uncaptured_pieces, possible_moves, winner = game.whose_turn(), game.get_uncaptured_pieces(), game.get_possible_moves(), game.get_winner()
            board_position = BoardPosition(whose_turn, uncaptured_pieces, possible_moves, winner, previous_board_position)
            board_positions.append(board_position)
            print(board_position)
        return board_positions
