import shogi
import numpy as np


def square_to_coord(s):
    col = s % 9
    row = s // 9
    return (col, row)

def diff(c1, c2):
    x1,y1 = c1
    x2,y2 = c2

    return  (x2 - x1, y2 - y1)

def sign(v):
    return -1 if v < 0 else (1 if v > 0 else 0)

# def mirror_move(move) - TODO

def result_to_int(result_str):
    if result_str == "1-0":
        return 1
    elif result_str == "0-1":
        return -1
    elif result_str == "1/2-1/2":
        return 0
    else:
        assert False, "bad result"

#def get_queen_dir

def queen_plane(diff):


def legal_moves(orig_board):
    '''
    action space is a 9x9x139 dimensional array
    Each of the 9x9 positions identify the square from which to "pick up" a piece. 

    The first 64 planes encode possible "queen moves" for any piece: a number of squares
    [1..8] in which the piece will be moved, along one of eight relative compass directions
    {N, NE, E, SE, S, SW, W, NW}.

    The next 2 planes encode knight moves for that piece. 

    An additional 64+2 planes for encoding promoting queen and knight moves.

    the last 7 planes encode a captured piece dropped back into board at that location.

    '''



