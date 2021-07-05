from __future__ import nested_scopes
from checkers_game import *
import numpy as np

cache = {} #you can use this to implement state caching!

# General function to get the number of black pieces on the board vs red 
def get_total_pieces(state):
    count_black = 0
    count_red = 0
    board = np.array(state.board)
    for i in board:
        for j in i:
            if j == 'r':
                count_red += 1
            elif j == 'R':
                count_red += 2
            elif j == 'b':
                count_black += 1
            elif j == 'B':
                count_black += 2

    return count_black, count_red

# Method to compute utility value of terminal state
def compute_utility(state, color):
    black, red = get_total_pieces(state)
    total_util = 0
    if(color == 'r'):
        total_util = red - black
    if(color == 'b'):
        total_util = black - red
    
    return total_util
        

# Better heuristic value of board
def compute_heuristic(state, color): 
    # IMPLEMENT
    return 0  # change this!


############ MINIMAX ###############################
def minimax_min_node(state, color, limit, caching=0):
    # IMPLEMENT
    return None, None


def minimax_max_node(state, color, limit, caching=0):
    # IMPLEMENT
    return None, None


def select_move_minimax(state, color, limit, caching=0):
    """
        Given a state (of type Board) and a player color, decide on a move.
        The return value is a list of tuples [(i1,j1), (i2,j2)], where
        i1, j1 is the starting position of the piece to move
        and i2, j2 its destination.  Note that moves involving jumps will contain
        additional tuples.

        Note that other parameters are accepted by this function:
        If limit is a positive integer, your code should enforce a depth limit that is equal to the value of the parameter.
        Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
        value (see compute_utility)
        If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
        If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    # IMPLEMENT
    return None


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(state, color, alpha, beta, limit, caching=0, ordering=0):
    # IMPLEMENT
    return None, None


def alphabeta_max_node(state, color, alpha, beta, limit, caching=0, ordering=0):
    # IMPLEMENT
    return None, None


def select_move_alphabeta(state, color, limit, caching=0, ordering=0):
    """
    Given a state (of type Board) and a player color, decide on a move. 
    The return value is a list of tuples [(i1,j1), (i2,j2)], where
    i1, j1 is the starting position of the piece to move
    and i2, j2 its destination.  Note that moves involving jumps will contain
    additional tuples.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enforce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    # IMPLEMENT
    return None


# ======================== Class GameEngine =======================================
class GameEngine:
    def __init__(self, str_name):
        self.str = str_name

    def __str__(self):
        return self.str

    # The return value should be a move that is denoted by a list
    def nextMove(self, state, alphabeta, limit, caching, ordering):
        global PLAYER
        PLAYER = self.str
        if alphabeta:
            result = select_move_alphabeta(Board(state), PLAYER, limit, caching, ordering)
        else:
            result = select_move_minimax(Board(state), PLAYER, limit, caching)

        return result
