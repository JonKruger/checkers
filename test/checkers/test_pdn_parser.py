import unittest
from checkers.pdn_parser import PDNParser

class TestPDNParser(unittest.TestCase):
    def test_parsing_full_game(self):
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
