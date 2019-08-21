import numpy as np
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

    def get_position_layout_2d(self, player):
        return self.state.get_position_layout_2d(player)

    def get_board_position_2d(self, player):
        result = np.tile(0, [self.state.board_height(), self.state.board_width()])
        position_layout_2d = self.get_position_layout_2d(player)

        for piece in self.state.get_uncaptured_pieces():
            x, y = np.argwhere(position_layout_2d == piece.position)[0]
            value = (3 if piece.king else 1) * (1 if piece.player == player else -1)
            result[x,y] = value
        return result

    def calculate_scores(self, winner, num_lookaheads=NUM_LOOKAHEADS):
        print(f'# moves: {len(self.state.moves)}, num_lookaheads: {num_lookaheads}')
        player_1_score = None
        player_2_score = None
        if self.state.is_over():
            # The game ended
            if (self.state.is_draw()): # draw
                player_1_score = 0
                player_2_score = 0
            else:
                player_1_score = 30. if winner == 1 else -30.
                player_2_score = 30. if winner == 2 else -30.
        else:
            raw_player_1_score = np.sum(self.get_board_position_2d(1))
            raw_player_2_score = np.sum(self.get_board_position_2d(2))

            if num_lookaheads > 0:
                possible_p1_move_outcomes = []
                possible_p2_move_outcomes = []
                possible_next_states = self.state.get_possible_next_states(actual_next_state=(self.actual_next_state.state if self.actual_next_state else None))
                print(f'there are {len(possible_next_states)} possible moves from here')
                for next_state in possible_next_states:
                    move = next_state.last_move()
                    next_state = State(next_state)
                    next_player_1_score, next_player_2_score = next_state.calculate_scores(winner, num_lookaheads - 1)

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

                    possible_p1_move_outcomes.append([player_1_score_diff, weighted_player_1_score_diff, None]) 
                    possible_p2_move_outcomes.append([player_2_score_diff, weighted_player_2_score_diff, None]) 
                
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
        
        return player_1_score, player_2_score

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

        for state in reversed(states):
            state.calculate_scores(winner)

        print(datetime.now() - start)
        