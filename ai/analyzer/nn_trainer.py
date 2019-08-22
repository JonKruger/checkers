import numpy as np
from datetime import datetime
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

        history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=200, batch_size=8).history
        predictions = model.predict(X_test)
        error = mean_absolute_error(y_test, predictions)
        print('MAE:', error)
        return history, y_test, predictions

    def get_model(self):
        if self._current_model is None:
            self._current_model = pickle.load(open('models/model.pickle.dat', 'rb'))
        return self._current_model


