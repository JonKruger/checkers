import numpy as np
from datetime import datetime
from ai.analyzer.weighted_win_likelihood_analyzer import State
from ai.analyzer.nn_trainer import NNTrainer

class ScoreBasedPlayer():
    def __init__(self, player_number):
        self._model = NNTrainer()
        self._player_number = player_number
    
    def select_move(self, game, possible_moves):
        start = datetime.now()

        possible_states = [State(game.move(move)) for move in possible_moves]

        if len(possible_states) == 1:
            best_state = possible_states[0]
        else:
            possible_state_scores = [self.predict_one(possible_state, self._player_number) for possible_state in possible_states]
            best_state = possible_states[np.argmax(possible_state_scores)]
            print(f'Predicting the best move using ScoreBasedPlayer took {datetime.now() - start}, scores: {[round(s,2) for s in possible_state_scores]}')
        return best_state.state.moves[-1]

    def predict_one(self, possible_state, my_player_number):
        possible_state.calculate_scores(None, lambda inner_state, player: State.calculate_raw_training_score(inner_state, player))
        return possible_state.get_score_for_player(my_player_number)
