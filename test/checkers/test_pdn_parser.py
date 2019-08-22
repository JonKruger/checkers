import unittest
from checkers.pdn_parser import PDNParser

class TestPDNParser(unittest.TestCase):
    def test_parsing_with_resgination(self):
        pdn = '''
                [Event "Test game"]
                [Date "1841-??-??"]
                [Black "Moorhead, W."]
                [White "Wyllie, J."]
                [Site "Manchester"]
                [Result "0-1"]
                1. 9-14 23-18 {this is a note} 2. 14x23 26x19
                {sometimes they put in random line breaks like this}
                3. 11-16 24-20 0-1
            '''
        game = PDNParser().parse(pdn)
        self.assertEqual(game.moves, [[9,14],[23,18],[14,23],[26,19],[11,16],[24,20]])
        self.assertEqual(game.get_winner(), 2)

    def test_parsing_partial_game(self):
        pdn = '''
                [Event "Test game"]
                [Date "1841-??-??"]
                [Black "Moorhead, W."]
                [White "Wyllie, J."]
                [Site "Manchester"]
                1. 9-14 23-18 {this is a note} 2. 14x23 26x19
                {sometimes they put in random line breaks like this}
                3. 11-16 24-20 
            '''
        game = PDNParser().parse(pdn)
        self.assertEqual(game.moves, [[9,14],[23,18],[14,23],[26,19],[11,16],[24,20]])
        self.assertIsNone(game.get_winner())
        self.assertFalse(game.is_over())
        self.assertFalse(game.is_draw())

    def test_implicit_double_jump(self):
        pdn = '''
                1. 9-13 23-19 2. 10-15 19x10 3. 6x15 26-23 4. 1-6 31-26 5. 6-10 24-19 6. 15x31 {actually 15x24x31 but they don't always spell it all out}
            '''
        game = PDNParser().parse(pdn) 
        self.assertEqual(game.moves, [[9,13],[23,19],[10,15],[19,10],[6,15],[26,23],[1,6],[31,26],[6,10],[24,19],[15,24],[24,31]])