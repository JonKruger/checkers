import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, MaxPooling2D
from keras.layers.convolutional import Conv2D
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pickle
from ai.analyzer.weighted_win_likelihood_analyzer import State

class NNTrainer():
    def __init__(self):
        self._current_model = None

    def train(self, weighted_states):
        seed = 1
        np.random.seed(seed)

        board_shape = tuple(weighted_states[0].state.get_position_layout_2d(1).shape)
        input_shape = (*board_shape, 1)
        X = np.array(list(map(lambda ws: ws.get_board_position_2d(), weighted_states)))
        X = X.reshape(X.shape[0], *input_shape)
        y = list(map(lambda ws: ws.weight, weighted_states))

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
        for state in possible_states:
            assert type(state) == State

        possible_positions = [s.get_board_position_2d(s.whose_turn()) for s in possible_states]
        reshaped_states = np.array(possible_positions).reshape(*np.array(possible_positions).shape, 1)
        model = self.get_model()

        # for now, just doing 1 move ahead
        predictions = model.predict(reshaped_states)
        #print(f'Made {predictions.shape[0]} predictions, min = {np.min(predictions)}, max = {np.max(predictions)}')
        return possible_states[np.argmax(predictions)]

    def get_model(self):
        if self._current_model is None:
            self._current_model = pickle.load(open('models/model.pickle.dat', 'rb'))
        return self._current_model


