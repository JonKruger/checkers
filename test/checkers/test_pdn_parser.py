import unittest
from checkers.pdn_parser import PDNParser

class TestPDNParser(unittest.TestCase):
    def test_parsing(self):
        pdn = '''
                [Event "Manchester 1841"]
                [Date "1841-??-??"]
                [Black "Moorhead, W."]
                [White "Wyllie, J."]
                [Site "Manchester"]
                [Result "0-1"]
                1. 11-15 24-20 {yeah I know these moves are actually not valid, I'm just testing parsing} 2. 19x12 26x17x10x1 0-1
            '''
        moves, result = PDNParser().parse(pdn)
        self.assertEqual(moves, [[11,15],[24,20],[19,12],[26,17],[17,10],[10,1]])
        self.assertEqual(result, '0-1')
        print('result', result)
