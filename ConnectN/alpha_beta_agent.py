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
        # Make decision
        curdepth = 0
        v, a = self.maxval(brd, -math.inf, math.inf, curdepth)
        return a                  # fix this later (arg(v))

    # Return maximum utility across all nodes
    def maxval(self, brd, alpha, beta, curdepth):
        if curdepth == self.max_depth:
            return self.utility(brd), -1               # fix this
        v = -math.inf
        action = -1
        brdactlist = self.get_successors(brd)
        for i in brdactlist:
            node_v, a = self.minval(i[0], alpha, beta, curdepth+1)
            if node_v > v:
                v = node_v
                action = i[1]
            if v >= beta:
                return v, a
            alpha = max(alpha, v)
        return v, action

    # Return minimum value across all nodes
    def minval(self, brd, alpha, beta, curdepth):
        if curdepth == self.max_depth:
            return self.utility(brd), -1  # fix this
        v = math.inf
        action = -1
        brdactlist = self.get_successors(brd)
        for i in brdactlist:
            node_v, a = self.maxval(i[0], alpha, beta, curdepth+1)
            if node_v < v:
                v = node_v
                action = i[1]
            if v <= alpha:
                return v, a
            beta = min(beta, v)
        return v, action

    # Returns utility of a given board
    def utility(self, brd):
        return random.randint(0, 100)


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
            succ.append((nb, col))
        return succ