from ai.players.random_ai_player import RandomAIPlayer
from ai.games.ai_game import AIGame
from checkers.game import Game
import random

class RandomAIGame(AIGame):
    def __init__(self, verbose=False):
        super().__init__(RandomAIPlayer(), RandomAIPlayer(), verbose) 
