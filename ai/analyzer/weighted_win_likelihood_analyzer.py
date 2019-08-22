import numpy as np
import multiprocessing as mp
from datetime import datetime
from checkers.game import Game
from checkers.board import Board

class State:
    MOVE_SELECTION_WEIGHT_FN = (lambda diff: 1.2 ** diff)
    ACTUAL_MOVE_BONUS = 0.5
    WINNING_SCORE = 30
    NUM_LOOKAHEADS = 4

    def __init__(self, state):
        self.state = state
        self.actual_next_state = None
        self.player_1_score = None
        self.player_2_score = None

        self._player_1_board_position_2d = None

    def get_position_layout_2d(self, player):
        return self.state.get_position_layout_2d(player)

    def get_board_position_2d(self, player):
        if self._player_1_board_position_2d is None:
            result = np.tile(0, [self.state.board_height(), self.state.board_width()])

            for piece in self.state.get_uncaptured_pieces():
                x = int((piece.position - 1) / 4)
                y = (piece.position - 1) % 4
                    
                value = (3 if piece.king else 1) * (1 if piece.player == 1 else -1)
                result[x,y] = value
            self._player_1_board_position_2d = result

        return self._player_1_board_position_2d if player == 1 else (Board.flip_2d(self._player_1_board_position_2d) * -1)

    def whose_turn(self):
        return self.state.whose_turn()

    def get_score_for_player(self, player_number):
        return self.player_1_score if player_number == 1 else self.player_2_score

    @classmethod
    def calculate_raw_training_score(cls, state, player):
        if state.state.is_over():
            # The game ended
            if (state.state.is_draw()): # draw
                return 0
            else:
                return 30. if state.state.get_winner() == player else -30.
        else:
            return np.sum(state.get_board_position_2d(player))

    def calculate_scores(self, winner, raw_score_fn, num_lookaheads=NUM_LOOKAHEADS):
        player_1_score = None
        player_2_score = None

        if self.state.whose_turn() == 1:
            raw_player_1_score = float(raw_score_fn(self, 1))
            raw_player_2_score = -raw_player_1_score
        else:
            raw_player_2_score = float(raw_score_fn(self, 2))
            raw_player_1_score = -raw_player_2_score

        if self.state.is_over():
            self.player_1_score = raw_player_1_score
            self.player_2_score = raw_player_2_score
        else:
            if num_lookaheads > 0:
                possible_p1_move_outcomes = []
                possible_p2_move_outcomes = []
                possible_next_states = self.state.get_possible_next_states(actual_next_state=(self.actual_next_state.state if self.actual_next_state else None))

                for next_state in possible_next_states:
                    possible_p1_move_outcome, possible_p2_move_outcome = self._calculate_possible_outcomes(next_state, winner, raw_score_fn, raw_player_1_score, raw_player_2_score, num_lookaheads)
                    possible_p1_move_outcomes.append(possible_p1_move_outcome)
                    possible_p2_move_outcomes.append(possible_p2_move_outcome)
                
                possible_p1_move_outcomes = np.array(possible_p1_move_outcomes)
                possible_p2_move_outcomes = np.array(possible_p2_move_outcomes)

                total_p1_weighted_score_diff = np.array(possible_p1_move_outcomes)[:,1].sum()
                total_p2_weighted_score_diff = np.array(possible_p2_move_outcomes)[:,1].sum()

                # Calculate the percentage likelihood that this move will be selected
                possible_p1_move_outcomes[:,2] = possible_p1_move_outcomes[:,1] / total_p1_weighted_score_diff
                possible_p2_move_outcomes[:,2] = possible_p2_move_outcomes[:,1] / total_p2_weighted_score_diff

                # The weight of this move is the score of this move + the likely diff in the score due to the upcoming potential moves
                player_1_score = raw_player_1_score + (possible_p1_move_outcomes[:,0] * possible_p1_move_outcomes[:,2]).sum()
                player_2_score = raw_player_2_score + (possible_p2_move_outcomes[:,0] * possible_p2_move_outcomes[:,2]).sum()
            else:
                player_1_score = raw_player_1_score
                player_2_score = raw_player_2_score

            self.player_1_score = player_1_score
            self.player_2_score = player_2_score
        
        return self.player_1_score, self.player_2_score

    def _calculate_possible_outcomes(self, next_state, winner, raw_score_fn, raw_player_1_score, raw_player_2_score, num_lookaheads):
        move = next_state.last_move()
        next_state = State(next_state)
        next_player_1_score, next_player_2_score = next_state.calculate_scores(winner, raw_score_fn, num_lookaheads - 1)

        player_1_score_diff = next_player_1_score - raw_player_1_score
        player_2_score_diff = next_player_2_score - raw_player_2_score

        # Account for the fact that people are more exponentially more likely to choose a 
        # move that gives them a better score.  This will reward good moves exponentially.
        weighted_player_1_score_diff = State.MOVE_SELECTION_WEIGHT_FN(player_1_score_diff)
        weighted_player_2_score_diff = State.MOVE_SELECTION_WEIGHT_FN(player_2_score_diff)

        # Give some extra reward/penalty to the move that was actually selected
        # based on whether the player won the game.  We're only going to give the
        # adjustment to the player that actually selected the move, not the other player.
        if self.actual_next_state is not None and move == self.actual_next_state.state.last_move() and winner is not None:
            if self.state.whose_turn() == 1:
                weighted_player_1_score_diff += (State.ACTUAL_MOVE_BONUS * (1 if winner == 1 else -1))
            if self.state.whose_turn() == 2:
                weighted_player_2_score_diff += (State.ACTUAL_MOVE_BONUS * (1 if winner == 2 else -1))

        return [player_1_score_diff, weighted_player_1_score_diff, None], [player_2_score_diff, weighted_player_2_score_diff, None]

class WeightedWinLikelihoodAnalyzer:
    def analyze_game(self, game):
        assert type(game) == Game

        weighted_states = self._calculate_game_weights(game)
        weight_values = list(map(lambda w: w.player_1_score, weighted_states)) 
        print(f'Weight values: count = {len(weight_values)}, mean = {np.mean(weight_values)}, std = {np.std(weight_values)}, 25% = {np.percentile(weight_values, 25)}, 75% = {np.percentile(weight_values, 75)}')

        return weighted_states

    def _calculate_game_weights(self, game):
        states = game.get_game_states()
        states = list(map(lambda s: State(s), states))
        for i in range(0, len(states) - 1):
            states[i].actual_next_state = states[i+1]
        self._calculate_weights(states, game.get_winner())
        return states

    def _calculate_weights(self, states, winner):
        start = datetime.now()

        for counter, state in enumerate(reversed(states)):
            print(f'Analyzing move {len(states) - counter} of {len(states)}')
            state.calculate_scores(winner, State.calculate_raw_training_score)

        print(datetime.now() - start)
        