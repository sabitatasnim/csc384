from __future__ import nested_scopes
from checkers_game import *
import numpy as np

cache = {} #you can use this to implement state caching!

# General function to get the number of black pieces on the board and red pieces 
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
    # get the total number of
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
    # return best_move and minimum utility value for the min node
    best_move = None
    util_value = 0
    min_util_value = float('inf')

    # Start caching 
    entry = (state.board, color)
    entry = str(entry)

    if caching and entry in cache.keys(): 
        return cache[entry]

    # First check and see who our opponent is 
    if color == 'r':
        opponent = 'b'
    elif color == 'b':
        opponent = 'r'

    # Check to see if the the limit is 0, that means we just return the utility value of the opponent (since we are a min node and the max nodes utility is needed)
    if limit == 0:
        util_value = compute_utility(state, opponent)
        #print("TERMINAL NODE ")
        return util_value, None

    # Check and see if we have any possible moves within the successors of the player
    player_successors = successors(state, color)

    # Check if there are any sucessors, if not return the utility of the opponent
    if len(player_successors) == 0:
        util_value = compute_utility(state, opponent)
        #print("TERMINAL NODE ")
        return util_value, None

    # Go through all sucessors to 
    for successor in player_successors:
        # get the utility from the max node
        max_util, max_move = minimax_max_node(successor, opponent, limit - 1, caching)
        
        # Once we find the lowest utility value, save that and the sucessor that it coresponds with
        if max_util < min_util_value:
            best_move = successor
            min_util_value = max_util
    
    # Check if in cache, if the entry not in cache, save it
    if best_move is not None and caching:
        if entry not in cache.keys():
            cache[entry] = min_util_value, best_move

    #print(player_successors)

    return min_util_value, best_move


def minimax_max_node(state, color, limit, caching=0):
    # IMPLEMENT
    # return best_move and utility value
    best_move = None
    util_value = 0
    max_util_value = float('-inf')

    # Start caching 
    entry = (state.board, color)
    entry = str(entry)

    if caching and entry in cache.keys(): 
        return cache[entry]

    # First check and see who our opponent is 
    if color == 'r':
        opponent = 'b'
    elif color == 'b':
        opponent = 'r'

    # Check and see if we are at the lowest utility 
    if limit == 0:
        util_value = compute_utility(state, color)
        #print("TERMINAL NODE ")
        return util_value, None

    # Check and see if we have any possible moves within the successors of the player
    player_successors = successors(state, color)

    # Check if there are any sucessors, if not then get the utility value of the current player because we are playing as max 
    if len(player_successors) == 0:
        util_value = compute_utility(state, color)
        return util_value, None

    # Go through all the sucessors and try to find the highest utility value to return and the coressponsing sucessor 
    for successor in player_successors:
        # get the utility from the max node
        min_util, min_move = minimax_min_node(successor, opponent, limit -1, caching)

        if min_util > max_util_value:
            best_move = successor
            max_util_value = min_util
    
    # Check if in cache, if the entry not in cache, save it
    if best_move is not None and caching:
        if entry not in cache.keys():
            cache[entry] = max_util_value, best_move

    #print(player_successors)

    return max_util_value, best_move


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
    # return the best move of the max from the minimax algorithm
    best_move = minimax_max_node(state, color, limit, caching)[1].move
    if best_move:
        return best_move
    else:
        return None


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(state, color, alpha, beta, limit, caching=0, ordering=0):
    # IMPLEMENT
    # return best_move and minimum utility value for the min node
    best_move = None
    util_value = 0
    min_util_value = float('inf')

    # Start caching 
    entry = (state.board, color)
    entry = str(entry)

    if caching and entry in cache.keys(): 
        return cache[entry]

    # First check and see who our opponent is 
    if color == 'r':
        opponent = 'b'
    elif color == 'b':
        opponent = 'r'
        
    # Check to see if the the limit is 0, that means we just return the utility value of the opponent (since we are a min node and the max nodes utility is needed)
    if limit == 0:
        util_value = compute_utility(state, opponent)
        #print("TERMINAL NODE ")
        return util_value, None

    # Check and see if we have any possible moves within the successors of the player
    player_successors = successors(state, color)

    # Check if there are any sucessors, if not return the utility of the opponent
    if len(player_successors) == 0:
        util_value = compute_utility(state, opponent)
        #print("TERMINAL NODE ")
        return util_value, None

    # Go through all sucessors to 
    for successor in player_successors:
        # get the utility from the max node
        max_util, max_move = alphabeta_max_node(successor, opponent, alpha, beta, limit - 1, caching, ordering)

        # Once we find the lowest utility value, save that and the sucessor that it coresponds with
        if max_util < min_util_value:
            best_move = successor
            min_util_value = max_util

        # Do alpha-beta pruning, if we see that the alpha value is greater than the max utility value we know we can just prune that branch
        if(alpha > max_util):
            return max_util, best_move

        beta = min(beta, max_util)

    # Check if in cache, if the entry not in cache, save it
    if best_move is not None and caching:
        if entry not in cache.keys():
            cache[entry] = min_util_value, best_move
     
    #print(player_successors)

    return min_util_value, best_move


def alphabeta_max_node(state, color, alpha, beta, limit, caching=0, ordering=0):
    # IMPLEMENT
    # return best_move and utility value
    best_move = None
    util_value = 0
    max_util_value = float('-inf')

    # Start caching 
    entry = (color, state.board)
    entry = str(entry)

    if caching and entry in cache.keys(): 
        return cache[entry]

    # First check and see who our opponent is 
    if color == 'r':
        opponent = 'b'
    elif color == 'b':
        opponent = 'r'

    # Check and see if we are at the lowest utility 
    if limit == 0:
        util_value = compute_utility(state, color)
        #print("TERMINAL NODE ")
        return util_value, None

    # Check and see if we have any possible moves within the successors of the player
    player_successors = successors(state, color)

    # Check if there are any sucessors, if not then get the utility value of the current player because we are playing as max 
    if len(player_successors) == 0:
        util_value = compute_utility(state, color)
        return util_value, None

    # Go through all the sucessors and try to find the highest utility value to return and the coressponsing sucessor 
    for successor in player_successors:
        # get the utility from the max node
        min_util, min_move = alphabeta_min_node(successor, opponent, alpha, beta, limit - 1, caching, ordering)

        if min_util > max_util_value:
            best_move = successor
            max_util_value = min_util

        # Do alpha-beta pruning and check if the minimum utility is greater than beta, which means we can prune an return current state
        if(min_util > beta):
            return min_util, best_move

        alpha = max(alpha, min_util)

    # Check if in cache, if the entry not in cache, save it
    if best_move is not None and caching:
        if entry not in cache.keys():
            cache[entry] = max_util_value, best_move

    #print(player_successors)

    return max_util_value, best_move


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
    # return the best move of the max from the minimax algorithm
    best_move = alphabeta_max_node(state, color, float("-inf"), float("inf"), limit, caching, ordering)[1].move
    if best_move:
        return best_move
    else:
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
