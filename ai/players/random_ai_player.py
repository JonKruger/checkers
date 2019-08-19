import random

class RandomAIPlayer():
    def select_move(self, game, possible_moves):
        return random.choice(possible_moves)
