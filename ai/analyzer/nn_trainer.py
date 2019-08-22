import numpy as np
from datetime import datetime
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, MaxPooling2D
from keras.layers.convolutional import Conv2D
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pickle
import multiprocessing as mp
from ai.analyzer.weighted_win_likelihood_analyzer import State

class NNTrainer():
    def __init__(self):
        self._current_model = None

    def train(self, weighted_states):
        seed = 1
        np.random.seed(seed)

        board_shape = tuple(weighted_states[0].state.get_position_layout_2d(1).shape)
        input_shape = (*board_shape, 1)
        X = np.array(list(map(lambda ws: ws.get_board_position_2d(1), weighted_states)) + list(map(lambda ws: ws.get_board_position_2d(2), weighted_states)))
        X = X.reshape(X.shape[0], *input_shape)
        y = list(map(lambda ws: ws.player_1_score, weighted_states)) + list(map(lambda ws: ws.player_2_score, weighted_states))

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed, shuffle=True)

        model = Sequential()
        model.add(Conv2D(32, kernel_size=(2, 2), strides=(1, 1), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Flatten())
        model.add(Dense(board_shape[0] * board_shape[1], activation='relu'))
        model.add(Dense(1, kernel_initializer='normal'))        
        model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['acc'])
        pickle.dump(model, open('./models/model.pickle.dat', 'wb'))
        NNTrainer.current_model = None # force model to reload

        history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, batch_size=8).history
        predictions = model.predict(X_test)
        error = mean_absolute_error(y_test, predictions)
        print('MAE:', error)
        return history, y_test, predictions

    def predict(self, possible_states):
        '''
        Predict the best move from a set of possible states.

        Parameters
        possible_states - an array of possible board states.  
        '''

        if len(possible_states) == 1:
            return possible_states[0]

        start = datetime.now()
        pool = mp.Pool(mp.cpu_count())
        possible_state_scores = pool.map(self.predict_one, [possible_state for possible_state in possible_states])
        pool.close()

        print(f'Predicting the best move took {datetime.now() - start}, scores: {[round(s,2) for s in possible_state_scores]}')
        return possible_states[np.argmax(possible_state_scores)]

    def predict_one(self, possible_state):
        possible_state.calculate_scores(None, lambda inner_state, player: State.calculate_raw_training_score(inner_state, player))
        return possible_state.current_player_score()

    def predict_raw_score(self, state, player):
        possible_position = state.get_board_position_2d(player)
        reshaped_state = np.array([possible_position]).reshape(1, *np.array(possible_position).shape, 1)
        model = self.get_model()
        return model.predict(reshaped_state)[0,0]

    def get_model(self):
        if self._current_model is None:
            self._current_model = pickle.load(open('models/model.pickle.dat', 'rb'))
        return self._current_model


