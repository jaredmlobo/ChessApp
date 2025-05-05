import sys
sys.path.append('/Users/jaredlobo/Documents/GitHub/ChessApp')

from game_logic import *
from pieces import *

def test_board_start_and_get_square():
    piece_pos = {
        'a8' : rook('b'), 'b8': knight('b'), 'c8': bishop('b'), 'd8': queen('b'), 'e8': king('b'), 'f8': bishop('b'), 'g8': knight('b'), 'h8': rook('b'),
        'h1' : rook('w'), 'b1': knight('w'), 'f1': bishop('w'), 'd1': queen('w'), 'e1': king('w'), 'c1': bishop('w'), 'g1': knight('w'), 'a1': rook('w'),      
    }
    
    new_game = game()

    for pos in piece_pos.keys():
        piec = new_game.board.get_square(pos)
        assert  str(piec) == str(piece_pos[pos])

def test_run_random_opening():
    new_game = game()

    new_game.execute_move_list([
        ('e2', 'e4'),
        ('d7', 'd5'),
        ('b1', 'c3'),
        ('d5', 'e4'),
        ('c3', 'e4'),
        ('e7', 'e5'),
        ('d2', 'd4'),
        ('e5', 'd4'),
        ('c2', 'c4'),
        ('d4', 'c3'),
        ('d1', 'd8')
    ])

    assert new_game.board.last_move == ('d1', 'd8')
    assert str(new_game.board.get_square('c3')) == str(pawn('b'))