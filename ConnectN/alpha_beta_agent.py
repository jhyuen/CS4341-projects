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
        print("V and action: ", v, a)
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
        points = 0

        print('h: '+ str(brd.h))
        print('w: '+ str(brd.w))
        for r in range(brd.h):
            for c in range(brd.w):
                tempPoints = 0
                piece = brd.board[r][c]
                if piece != 0:
                    print('piece: ' + str(piece))
                
                # Check for 2,3,4,...,n
                for n in range(brd.n,1,-1):
                    if piece != 0:
                        print('n: ' + str(n))
                        print('r: ' + str(r) + ' c: ' + str(c))

                    if piece == 1: # Player 1
                        tempPoints += (self.is_any_n_line_at(brd,c,r,n,1) * (n-1))
                    else: # Player 2
                        tempPoints += (self.is_any_n_line_at(brd,c,r,n,2) * (n-1) * -1)

                points = points + tempPoints
                
        # print("Points :", points)
        # brd.print_it()
        print('points: ' + str(points))
        return points
        # return random.randint(0, 100)


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
    # RETURN [Bool]: True if n tokens of the same type have been found, False otherwise EDIT
    def is_n_line_at(self, brd, x, y, dx, dy, n, p):
        """Return True if a line of identical tokens exists starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + (n-1) * dx >= brd.w) or
            (y + (n-1) * dy < 0) or (y + (n-1) * dy >= brd.h)):
            return False
        # Get token at (x,y)
        # print(str(x)+ ' ' + str(y))
        #t = brd.board[y][x]

        # Go through elements
        for i in range(1, n):
            if brd.board[y + i*dy][x + i*dx] != p:
                return False
        return True

    # Check if a line of identical tokens exists starting at (x,y) in any direction
    #
    # PARAM [board] board: the board for a given game
    # PARAM [int] x: the x coordinate of the starting cell
    # PARAM [int] y: the y coordinate of the starting cell
    # PARAM [int] n: the number of tokens in a row
    # PARAM [int] p: player token number
    # RETURN [Bool]: True if n tokens of the same type have been found, False otherwise EDIT
    def is_any_n_line_at(self, brd, x, y, n, p):
        """ Return number of lines of identical tokens starting at (x,y) 
            in any direction that satisfy the given number """
        lines = 0
        if self.is_n_line_at(brd, x, y, 1, 0, n, p): # Horizontal
            lines += 1
        if self.is_n_line_at(brd, x, y, 0, 1, n, p): # Vertical
            lines += 1
        if self.is_n_line_at(brd, x, y, 1, 1, n, p): # Diagonal up
            lines += 1
        if self.is_n_line_at(brd, x, y, 1, -1, n, p): # Diagonal down
            lines += 1

        return lines
            