# This is necessary to find the main code
import sys
import math
# import numpy as np
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity


class QCharacter(CharacterEntity):
    # TODO: move all code into TestCharacter

    filename = ""

    def setFilename(self, filename):
        self.filename = filename

    def do(self, wrld):
        # read w from file
        f = open(self.filename, 'r')
        w = list(map(int, f.read().split(" ")))
        f.close()

        # stores optimal action list
        actlist = self.optiact(wrld, w)

        self.move(actlist[0], actlist[1])
        if actlist[2]:
            self.place_bomb()

        # TODO: check if the game has ended (done() function)

        # calculate rewards for the action
        # TODO: figure out what wrld.me() does and what role the character plays
        r = self.reward(wrld.me(self), actlist[4], actlist[5])

        new_w = self.Qlearning(wrld, actlist[0], actlist[1], actlist[2], actlist[4], r, w)

        # write to file
        f = open("variant1.txt", "w")
        f.write(' '.join(str(x) for x in new_w))
        f.close()
        pass


    # given a world configuration, returns a list for optimal actions and highest Q value
    # in order of [dx, dy, bomb?, Q, newwrld, events]
    def optiact(self, wrld, w):
        #
        # Get first character in the world
        m = next(iter(wrld.characters().values()))

        # keep track of highest Q value so far
        Q = -math.inf

        # stores best move for the character, in order of [dx, dy, bomb?, maxQ, newwrld, events]
        # default value moves toward down right and places the bomb
        # TODO: reset default value or figure out better way to initialize values
        action = [1, 1, True, Q, wrld.next(), []]

        # Go through the possible 8-moves of the character and placing the bomb

        # loop through whether or not placing the bomb
        # TODO: check what would happen if a bomb has already been placed by the character
        for bomb in [True, False]:
            # Loop through delta x
            for dx in [-1, 0, 1]:
                # Avoid out-of-bound indexing
                if (m.x + dx >= 0) and (m.x + dx < wrld.width()):
                    # Loop through delta y
                    for dy in [-1, 0, 1]:
                        # Make sure the character is moving
                        if (dx != 0) or (dy != 0):
                            # Avoid out-of-bound indexing
                            if (m.y + dy >= 0) and (m.y + dy < wrld.height()):
                                # No need to check impossible moves
                                if not wrld.wall_at(m.x + dx, m.y + dy):
                                    # Set move in wrld
                                    m.move(dx, dy)
                                    # Get new world
                                    (newwrld, events) = wrld.next()
                                    # calculate approximate Q value for the new world state
                                    newQ = self.approxQ(newwrld, events, dx, dy, bomb, w)
                                    # if new Q value is greater than previous, update optimal actions
                                    if newQ > Q:
                                        action[0] = dx
                                        action[1] = dy
                                        action[2] = bomb
                                        action[3] = newQ
                                        action[4] = newwrld
                                        action[5] = events
        return action



    # returns score for certain character given a world and events
    # TODO: finish defining reward function
    def reward(self, char, wrld, events):
        return 0

    # returns approximate Q value given a world state and the actions the character took
    # TODO: finish calculating approximate Q value
    def approxQ(self, wrld, events, dx, dy, bomb, w):
        # Q = w1*f1(s, a) + ...
        Q = 0
        return Q

    # updates w values after each action
    def Qlearning(self, wrld, dx, dy, bomb, newwrld, r, w):
        alpha = 0.95
        gamma = 0.9

        # update w values
        delta = (r + gamma * self.optiact(newwrld, w)[3]) - self.approxQ(wrld, events, dx, dy, bomb, w)
        new_w = []
        for i in range(len(w)):
            new_w[i] = w[i] + alpha * delta * f
        return new_w

