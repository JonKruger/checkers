import numpy as np
from datetime import datetime
from ai.analyzer.weighted_win_likelihood_analyzer import State
from ai.analyzer.nn_trainer import NNTrainer
from checkers.game import Game

class NNPlayer():
    def __init__(self, player_number):
        self._model = NNTrainer()
        self._player_number = player_number
    
    def select_move(self, game, possible_moves):
        for possible_move in possible_moves:
            assert type(possible_move) == list and len(possible_move) == 2

        possible_states = [State(game.move(move)) for move in possible_moves]
        best_state = self.predict(possible_states)
        assert type(best_state) == State
        return best_state.state.moves[-1]

    def predict(self, possible_states):
        '''
        Predict the best move from a set of possible states.

        Parameters
        possible_states - an array of possible game states.  
        '''
        for possible_state in possible_states:
            assert type(possible_state) == State, type(possible_state)

        if len(possible_states) == 1:
            return possible_states[0]

        start = datetime.now()

        possible_state_scores = []
        for possible_state in possible_states:
            possible_state_scores.append(self._predict_one(possible_state))

#        all_possible_states_with_lookahead = self._get_all_possible_next_states(possible_states)
#        predicted_raw_scores = self._predict_raw_scores(all_possible_states_with_lookahead, self._player_number)

#        possible_state_scores = [self._predict_one_with_cached_predictions(possible_state, predicted_raw_scores) for possible_state in possible_states]

        print(f'Predicting the best move using NNTrainer took {datetime.now() - start}, scores: {[round(s,2) for s in possible_state_scores]}')
        return possible_states[np.argmax(possible_state_scores)]

    def _predict_raw_scores(self, possible_states, player):
        for possible_state in possible_states:
            assert type(possible_state) == State, type(possible_state)

        possible_positions = [state.get_board_position_2d(player) for state in possible_states]
        reshaped_state = np.array(possible_positions).reshape(*np.array(possible_positions).shape, 1)
        predictions = self._model.get_model().predict(reshaped_state)[:,0]

        predicted_raw_scores = {}
        for i in range(len(possible_states)):
            predicted_raw_scores[possible_states[i].state] = predictions[i]
        return predicted_raw_scores

    def _predict_one(self, possible_state):
        assert type(possible_state) == State
        possible_position = possible_state.get_board_position_2d(self._player_number)
        reshaped_state = np.array([possible_position]).reshape(1, *np.array(possible_position).shape, 1)
        possible_state.calculate_scores(None, lambda state, player: self._model.get_model().predict(reshaped_state)[0,0])
        return possible_state.get_score_for_player(self._player_number)

    def _predict_one_with_cached_predictions(self, possible_state, predicted_raw_scores):
        assert type(possible_state) == State
        possible_state.calculate_scores(None, lambda state, player: predicted_raw_scores[state.state])
        return possible_state.get_score_for_player(self._player_number)

    def _get_all_possible_next_states(self, possible_states, num_lookaheads=(State.NUM_LOOKAHEADS-1)):
        for possible_state in possible_states:
            assert type(possible_state) == State

        next_states = possible_states.copy()
        if num_lookaheads > 0:
            for next_state in next_states:
                next_next_states = list(map(lambda state: State(state), next_state.state.get_possible_next_states()))
                next_states = next_states + self._get_all_possible_next_states(next_next_states, num_lookaheads - 1)
        return next_states
