import unittest
import numpy as np
from checkers.game import Game
from test.test_helpers.game_test_helper import GameTestHelper

class TestGame(unittest.TestCase):

    def test_piece_locations_for_new_game(self):
        game = Game()

        player_1_pieces = game.board.get_player_pieces(1)
        player_2_pieces = game.board.get_player_pieces(2)

        self.assertEqual(len(player_1_pieces), 12)
        self.assertEqual(len(player_2_pieces), 12)

        self.assertListEqual(list(map(lambda p: p.position, player_1_pieces)), list(range(1,13)))
        self.assertListEqual(list(map(lambda p: p.position, player_2_pieces)), list(range(21,33)))

    def test_piece_locations_for_new_game_different_board_size(self):
        game = Game(width=5, height=6, rows_per_user_with_pieces=2)

        player_1_pieces = game.board.get_player_pieces(1)
        player_2_pieces = game.board.get_player_pieces(2)

        self.assertEqual(len(player_1_pieces), 10)
        self.assertEqual(len(player_2_pieces), 10)

        self.assertListEqual(list(map(lambda p: p.position, player_1_pieces)), list(range(1,11)))
        self.assertListEqual(list(map(lambda p: p.position, player_2_pieces)), list(range(21,31)))

    def test_moving_creates_a_copy_of_everything(self):
        game1 = GameTestHelper()
        game1.board.set_pieces(['B 25','W 6','B 4'], 1)

        # Make a move...
        game2 = game1.move([4,8])

        # Since making a move created a copy of everything, we can do a different move with game1
        # since things should still be in the same state as it was before we did the 4-8 move.
        # This move will create a king, so we can test that game2 doesn't have any kings.
        game3 = game1.move([25,29])

        # testing game2
        black_pieces = game2.board.get_player_pieces(1)
        self.assertListEqual(list(map(lambda p: p.position, black_pieces)), [8,25])
        self.assertListEqual(list(map(lambda p: p.king, black_pieces)), [False,False])

        # testing game3
        black_pieces = game3.board.get_player_pieces(1)
        self.assertListEqual(list(map(lambda p: p.position, black_pieces)), [4,29])
        self.assertListEqual(list(map(lambda p: p.king, black_pieces)), [False,True])

    def test_game_states_reference_each_other(self):
        game1 = Game()
        game2 = game1.move([11,16])
        self.assertEqual(game2.previous_state, game1)

    def test_get_game_states(self):
        game1 = Game()
        game2 = game1.move([11,16])
        game3 = game2.move([24,20])
        self.assertEqual(game3.get_game_states(), [game1, game2, game3])

    def test_last_move(self):
        game1 = Game()
        self.assertIsNone(game1.last_move())

        game2 = game1.move([11,16])
        self.assertEqual(game2.last_move(), [11,16])

    def test_get_possible_next_states(self):
        game1 = Game()
        game2 = game1.move([11,16])

        next_states = game1.get_possible_next_states(actual_next_state=game2)
        self.assertEqual(len(next_states), 7)
        self.assertEqual(type(next_states[0]), Game)

        actual_next_state = next(s for s in next_states if s.last_move() == [11,16])
        self.assertEqual(actual_next_state, game2)

    def test_get_possible_next_states_new_actual_next_state(self):
        # re-do the same move, pass in a new actual_next_state
        game1 = Game()
        game2_1 = game1.move([11,16])
        next_states = game1.get_possible_next_states(actual_next_state=game2_1)

        game2_2 = game1.move([11,16])
        next_states = game1.get_possible_next_states(actual_next_state=game2_2)
        self.assertEqual(len(next_states), 7)

        actual_next_state = next(s for s in next_states if s.last_move() == [11,16])
        self.assertEqual(actual_next_state, game2_2)

    def test_get_possible_next_states_force_reload(self):
        game1 = Game()
        game2 = game1.move([11,16])

        # force_reload = True
        next_states = game1.get_possible_next_states(actual_next_state=game2, force_reload=True)
        self.assertEqual(len(next_states), 7)
        self.assertEqual(type(next_states[0]), Game)

        actual_next_state = next(s for s in next_states if s.last_move() == [11,16])
        self.assertEqual(actual_next_state, game2)
