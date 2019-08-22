import numpy as np
import re
import tqdm
from checkers.game import Game

class PDNParser():
    def parse(self, text):
        text = self._find_move_data(text)
        text = re.sub(r'[0-9]+\. ', '', text)
        splits = text.split(' ')
        moves, result = self._parse_moves(splits)
        game = self._replay_game(moves, result)
        return game

    def _parse_moves(self, splits):
        moves = []
        game_result = None
        for s in splits:
            parsed_move, parsed_game_result = self._parse_move(s)

            if parsed_game_result is not None:
                game_result = parsed_game_result

            if parsed_move is None:
                continue
            elif type(parsed_move[0]) == int:
                moves.append(parsed_move)
            elif type(parsed_move[0] == list):
                for inner_move in parsed_move:
                    moves.append(inner_move)
            else:
                raise Exception(f'Unable to parse move: {s}')

        return moves, game_result

    def _parse_move(self, s):
        s = s.strip()
        if (s == '0-1' or s == '1-0' or s == '1/2-1/2'):
            return None, s
        elif '-' in s:
            return list(map(int, s.split('-'))), None
        elif 'x' in s:
            jump_splits = list(map(int, s.split('x')))
            moves = []
            for i in range(0, len(jump_splits) - 1):
                moves.append([jump_splits[i], jump_splits[i + 1]])
            return moves, None
        raise Exception(f'Unable to parse move: {s}')

    def _find_move_data(self, text):
        data = None
        for line in text.split('\n'):
            if any([x in line for x in ('[', ']')]):
                continue
            line = line.strip().lower()
            if line.startswith('1.'):
                data = ""
            elif data is None:
                continue
            if line:
                data += " {}".format(line)
            if not line:
                break
        
        return re.sub(r" \{[^\}]+\}", "", data.strip().lower())

    def _replay_game(self, moves, result):
        game = Game()
        for move in moves:
            game = game.move(move)

        if result == '0-1' and game.get_winner() != 2:
            game = game.resign(resigning_player=1)
        elif result == '1-0' and game.get_winner() != 1:
            game = game.resign(resigning_player=2)
        elif result == '1/2-1/2' and game.is_draw() == False:
            game = game.agree_to_draw()

        return game