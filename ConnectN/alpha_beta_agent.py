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
        print("Points: " + str(v))
        print("Action: " + str(a))

        return a

    # Return maximum utility across all nodes
    def maxval(self, brd, alpha, beta, curdepth):
        if curdepth == self.max_depth:
            return self.utility(brd), -1               
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
        points = 0

        player = 1
        opponent = 2

        if brd.player == 1:
            player == brd.player
            opponent == 2
        else:
            player = brd.player
            opponent = 1

        for r in range(brd.h):
            for c in range(brd.w):
                points += self.checkLines(brd,c,r,brd.n,player,opponent)

        return points


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


    # Check if a line of identical tokens exists starting at (x,y) in direction (dx,dy)
    #
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # PARAM [int] dx: the step in the x direction
    # PARAM [int] dy: the step in the y direction
    # PARAM [int] p: player token number
    # RETURN [int]: True if n tokens of the same type have been found, False otherwise EDIT
    def connectNCheck(self, brd, x, y, dx, dy, n, p, o):
        """ """
        # Avoid out-of-bounds errors
        if ((x + (n-1) * dx >= brd.w) or
            (y + (n-1) * dy < 0) or (y + (n-1) * dy >= brd.h)):
            return 0

        # Get token at (x,y)
        # print(str(x)+ ' ' + str(y))

        playerTokens = 0
        opponentTokens = 0
        spaceTokens = 0

        # piece  = brd.board[y][x]
        for i in range(0, n):
            target = brd.board[y + i*dy][x + i*dx]
            if target == p:
                playerTokens += 1
            elif target == o:
                opponentTokens += 1
            else:
                spaceTokens += 1
        
        # Evaluate line
        if spaceTokens == n:
            return 0
        elif playerTokens == n:
            return 100000
        elif opponentTokens == n:
            return -100000
        elif (playerTokens > 0) and (opponentTokens > 0):
            return 0
        elif (playerTokens > 0) and (opponentTokens == 0):
            return playerTokens*n
        elif (opponentTokens > 0) and (playerTokens == 0):
            return opponentTokens*n*-1
        else:
            return 0

    # Check if a line of identical tokens exists starting at (x,y) in any direction
    #
    # PARAM [board] board: the board for a given game
    # PARAM [int] x: the x coordinate of the starting cell
    # PARAM [int] y: the y coordinate of the starting cell
    # PARAM [int] n: the number of tokens in a row
    # PARAM [int] p: player token number
    # RETURN [Bool]: True if n tokens of the same type have been found, False otherwise EDIT
    def checkLines(self, brd, x, y, n, p, o):
        """ """
        points = 0
        points += self.connectNCheck(brd, x, y, 1, 0, n, p, o) # Horizontal
        points += self.connectNCheck(brd, x, y, 0, 1, n, p, o) # Vertical
        points += self.connectNCheck(brd, x, y, 1, 1, n, p, o) # Diagonal up
        points += self.connectNCheck(brd, x, y, 1, -1, n, p, o) # Diagonal down
        return points
            