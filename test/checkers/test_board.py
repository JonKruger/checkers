import unittest
import numpy as np
from copy import deepcopy
from checkers.board import Board
from checkers.game import Game

class TestBoard(unittest.TestCase):
    def test_position_layout_2d(self):
        board = Game().board
        np.testing.assert_array_equal(board.position_layout_2d, np.array([[ 1,  2,  3,  4],[ 5,  6,  7,  8],[ 9, 10, 11, 12],[13, 14, 15, 16],[17, 18, 19, 20],[21, 22, 23, 24],[25, 26, 27, 28],[29, 30, 31, 32]]))

    def test_flip(self):
        board = Game().board
        self.assertEqual(board.flip_position(32), 1)
        self.assertEqual(board.flip_position(1), 32)
        self.assertEqual(board.flip_position(29), 4)
        self.assertEqual(board.flip_position(4), 29)
        self.assertEqual(board.flip_position(19), 14)
        self.assertEqual(board.flip_position(14), 19)

