import unittest
from checkers.game import Game

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

