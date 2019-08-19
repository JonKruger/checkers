import random

class RandomAIPlayer():
    def move(self, possible_moves):
        return random.choice(possible_moves)
