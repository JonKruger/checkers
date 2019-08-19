from ai.analyzer.weighted_win_likelihood_analyzer import State
from ai.analyzer.nn_trainer import NNTrainer

class NNPlayer():
    def __init__(self, model):
        self._model = model
    
    def move(self, game, possible_moves):
        possible_states = [State(game.move(move)) for move in possible_moves]
        best_state = NNTrainer().predict(possible_states)
        return best_state.moves[-1]
