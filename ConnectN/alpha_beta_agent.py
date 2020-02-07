import math
import agent
import board
import random

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here

        # Read board


        # Interpret using heurisitcs
        # Create graph and load in heuristics

        # Interpret using heurisitcs - Winny - make fake heuristics
        # Create graph and load in heuristics - We'll figure it out
        # Create graph class - Joe

        # Call alpha beta on graph - Mei

        # Make decision
        v = self.maxval(brd, -math.inf, math.inf)
        return v                     # fix this later (arg(v))

    # Return maximum utility across all nodes
    def maxval(self, brd, alpha, beta):
        if self.tertest(brd):
            return self.utility(brd)               # fix this
        v = -math.inf
        for i in range(brd.w):
            v = max(v, self.minval(brd, alpha, beta))           # fix this
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    # Return minimum value across all nodes
    def minval(self, brd, alpha, beta):
        if self.tertest(brd):
            return self.utility(brd)  # fix this
        v = math.inf
        for i in range(brd.w):
            v = min(v, self.maxval(brd, alpha, beta))  # fix this
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Determines whether a node is in terminal state
    def tertest(self, brd):
        return True

    # Returns utility of a given board
    def utility(self, brd):
        return 0


    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ
