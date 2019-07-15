import unittest
from test.test_helpers.board_test_helper import BoardTestHelper

class TestBoardTestHelper(unittest.TestCase):
    def test_parse_piece_notation_black(self):
        piece = BoardTestHelper.parse_piece_notation('B 3')
        assert str(piece) == 'B 3'

    def test_parse_piece_notation_white(self):
        piece = BoardTestHelper.parse_piece_notation('W 32')
        assert str(piece) == 'W 32'

    def test_parse_piece_notation_king(self):
        piece = BoardTestHelper.parse_piece_notation('W king 11')
        assert str(piece) == 'W king 11'        