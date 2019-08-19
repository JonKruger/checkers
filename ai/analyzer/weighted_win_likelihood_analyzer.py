import numpy as np
from checkers.game import Game
from checkers.board import Board

class State:
    def __init__(self, state):
        self.state = state

    def get_position_layout_2d(self):
        return self.state.get_position_layout_2d(flip_for_white=True)

    def get_board_position_2d(self):
        result = np.tile(0, [self.state.board.height, self.state.board.width])
        position_layout_2d = self.get_position_layout_2d()
        whose_turn = self.state.whose_turn()

        for piece in self.state.get_uncaptured_pieces():
            x, y = np.argwhere(position_layout_2d == piece.position)[0]
            value = (3 if piece.king else 1) * (1 if piece.player == whose_turn else -1)
            result[x,y] = value
        return result

    def calculate_score(self):
        if self.state.is_over():
            # The game ended
            if (self.state.is_draw()): # draw
                weight = 0
            else:
                weight = 100. if self.state.get_winner() == self.state.whose_turn() else -100.
        else:
            weight = np.sum(self.get_board_position_2d())
        return weight

class WeightedState(State):
    def __init__(self, state, weight):
        assert type(weight) != int, type(weight)
        super().__init__(state)      
        self.weight = weight

class WeightedWinLikelihoodAnalyzer:
    def analyze_game(self, game):
        # Replay the game, taking note of the board after each move
        # Work backwards - for each board position, what are the possible moves, and what is the likelihood of a win in that position?

        weights = self._calculate_game_weights(game)
        weight_values = list(map(lambda w: w.weight, weights))
        print(f'Weight values: count = {len(weight_values)}, mean = {np.mean(weight_values)}, std = {np.std(weight_values)}, 25% = {np.percentile(weight_values, 25)}, 75% = {np.percentile(weight_values, 75)}')

        return weights
        
    def _get_game_states(self, moves):
        game = Game()
        states = [game]

        for move in moves:
            game = game.move(move)
            states.append(game)

        return states

    def _calculate_game_weights(self, game):
        states = game.get_game_states()
        weights = {1:[],2:[]} # one array for each player
        self._calculate_weights(states, weights)
        all_weights = weights[1] + weights[2]
        return all_weights       

    def _calculate_weights(self, states, weights):
        state = states[-1] # start with the last move that we have and work backwards

        if state.is_over():
            weight = State(state).calculate_score()
        else:
            possible_move_weights = []
            for move in state.get_possible_moves():
                next_state = state.move(move)
                possible_move_weights.append(State(next_state).calculate_score())
            weight = np.mean(possible_move_weights)
        
        if state.whose_turn() == 1:
            weights[1].append(WeightedState(state, weight))
            weights[2].append(WeightedState(state, weight * -1))
        elif state.whose_turn() == 2:
            weights[1].append(WeightedState(state, weight * -1))
            weights[2].append(WeightedState(state, weight))

        # Go back to the previous move and calculate its weights
        if (len(states) > 1):
            self._calculate_weights(states[0:-1], weights)


    
