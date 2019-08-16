from ai.players.random_ai_player import RandomAIPlayer
from checkers.game import Game
import random

class RandomAIGame:
    def __init__(self):
        self._black = RandomAIPlayer()
        self._white = RandomAIPlayer()
        self._game = Game()

    def play(self):
        while self._game.is_over() == False:
            print(f"It's {'Black' if self._game.whose_turn() == 1 else 'White'}'s turn")
            num_possible_moves = len(self._game.get_possible_moves())
            print(f'There are {num_possible_moves} possible moves')

            moves = self._game.get_possible_moves()
            move = random.choice(moves)
            print(f'Moving {move}')
            self._game = self._game.move(move)
        print(f"Winner is {'Black' if self._game.get_winner() == 1 else 'White'}!")
        print(self._game.moves)
        return self._game.moves, self._game.get_winner()
