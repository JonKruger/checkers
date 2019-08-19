from ai.players.random_ai_player import RandomAIPlayer
from checkers.game import Game
import random

class AIGame:
    def __init__(self, black_player, white_player, verbose=False):
        self._black = black_player
        self._white = white_player
        self._game = Game()
        self._verbose = verbose

    def play(self):
        while self._game.is_over() == False:

            if self._verbose:
                print(f"It's {'Black' if self._game.whose_turn() == 1 else 'White'}'s turn") 
            
            num_possible_moves = len(self._game.get_possible_moves())
            
            if self._verbose:
                print(f'There are {num_possible_moves} possible moves') 

            moves = self._game.get_possible_moves()
            move = self.current_turn_player().select_move(self._game, moves)
            if self._verbose:
                print(f'Moving {move}') 
            self._game = self._game.move(move)
        
        if self._verbose:
            print(f"Winner is {'Black' if self._game.get_winner() == 1 else 'White'}!") 
            print(self._game.moves) 
        
        return self._game.moves, self._game.get_winner()
    
    def current_turn_player(self):
        return self._black if self._game.whose_turn() == 1 else self._white
