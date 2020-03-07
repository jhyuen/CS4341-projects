# This is necessary to find the main code
import sys
import math
import numpy as np
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from events import Event


class QCharacter(CharacterEntity):
    # TODO: move all code into TestCharacter

    filename = ""

    def setFilename(self, filename):
        self.filename = filename

    def do(self, wrld):
        # read w from file
        f = open(self.filename, 'r')
        w = list(map(float, f.read().split(" ")))
        f.close()

        # grid = self.get_world_grid(wrld)
        # path = astar(grid, (0, 0), (18, 7))
        # print(path)
        # print(len(path))

        # stores optimal action list
        actlist = self.optiact(wrld, w)

        self.move(actlist[0], actlist[1])
        if actlist[2]:
            self.place_bomb()

        # TODO: check if the game has ended (done() function)

        # calculate rewards for the action
        r = self.reward(actlist[4], actlist[5])

        new_w = self.Qlearning(wrld, actlist[0], actlist[1], actlist[2], actlist[4], r, w)

        # write to file
        f = open(self.filename, "w")
        f.write(' '.join(str(x) for x in new_w))
        f.close()
        pass


    # given a world configuration, returns a list for optimal actions and highest Q value
    # in order of [dx, dy, bomb?, Q, newwrld, events]
    def optiact(self, wrld, w):
        #
        # Get first character in the world
        m = wrld.me(self)

        # keep track of highest Q value so far
        Q = -math.inf

        # stores best move for the character, in order of [dx, dy, bomb?, maxQ, newwrld, events]
        # default value moves toward down right and places the bomb
        # TODO: reset default value or figure out better way to initialize values
        action = [1, 1, True, Q, wrld.next(), []]

        # Go through the possible 8-moves of the character and placing the bomb

        # loop through whether or not placing the bomb
        # TODO: check what would happen if a bomb has already been placed by the character
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
                                newQ = self.approxQ(newwrld, dx, dy, False, w)
                                # if new Q value is greater than previous, update optimal actions
                                if newQ[0] > Q:
                                    action[0] = dx
                                    action[1] = dy
                                    action[2] = False
                                    action[3] = newQ[0]
                                    action[4] = newwrld
                                    action[5] = events
                    elif dx == 0 and dy == 0:
                        # Set move in wrld
                        m.move(dx, dy)
                        # Get new world
                        (newwrld, events) = wrld.next()

                        # calculate approximate Q value for the new world state
                        newQ = self.approxQ(newwrld, dx, dy, True, w)
                        # if new Q value is greater than previous, update optimal actions
                        if newQ[0] > Q:
                            action[0] = dx
                            action[1] = dy
                            action[2] = True
                            action[3] = newQ[0]
                            action[4] = newwrld
                            action[5] = events
        return action



    # returns score for certain character given a world and events
    # TODO: finish defining reward function
    def reward(self, wrld, events):
        r = 0

        for e in events:
            if e.tpe == Event.BOMB_HIT_WALL:
                if e.character == self:
                    r = r + 10
            elif e.tpe == Event.BOMB_HIT_MONSTER:
                if e.character == self:
                    r = r + 50
            elif e.tpe == Event.BOMB_HIT_CHARACTER:
                if e.character == self:
                    r = r + 100


        return r

    # returns approximate Q value given a world state and the actions the character took
    # TODO: finish calculating approximate Q value
    def approxQ(self, wrld, dx, dy, bomb, w):
        # Q = w1*f1(s, a) + ...

        f = []

        next_bombs = []
        next_explosions = []
        next_walls = []
        next_characters = []
        next_monsters = []
        next_exit_row = -1
        next_exit_col = -1

        for row in range(wrld.height()):
            for col in range(wrld.width()):
                if wrld.empty_at(col, row):
                    pass
                elif wrld.exit_at(col, row):
                    next_exit_row = row
                    next_exit_col = col
                elif wrld.wall_at(col, row):
                    next_walls.append((col, row))
                elif wrld.bomb_at(col, row):
                    next_bombs.append((col, row))
                elif wrld.explosion_at(col, row):
                    next_explosions.append((col, row))
                elif wrld.monsters_at(col, row):
                    next_monsters.append((col, row))
                elif wrld.characters_at(col, row):
                    next_characters.append((col, row))

        grid = self.get_world_grid(wrld).astype(int)

        f.append(self.distance_to_exit(wrld, (next_exit_col, next_exit_row), grid))
        f.append(self.distance_to_closest_monster(wrld, next_monsters, grid))
        f.append(self.angle_between_closest_monster_and_exit(wrld, (next_exit_col, next_exit_row), next_monsters, grid))
        f.append(self.timer_of_closest_bomb(wrld, next_bombs, grid))
        f.append(self.distance_to_closest_bomb(wrld, next_bombs, grid))
        f.append(self.distance_to_explosion(wrld, next_explosions, grid))
        f.append(self.distance_to_closest_wall(wrld, next_walls, grid))
        f.append(self.distance_to_closest_character(wrld, next_characters, grid))
        
        Q = 0
        for i in range(0, len(w)):
            Q += w[i]*f[i]

        return Q, f

    # updates w values after each action
    def Qlearning(self, wrld, dx, dy, bomb, newwrld, r, w):
        alpha = 0.95
        gamma = 0.9

        Q, f = self.approxQ(wrld, dx, dy, bomb, w)

        # update w values
        delta = (r + gamma * self.optiact(newwrld, w)[3]) - Q
        new_w = np.zeros(len(w))
        for i in range(len(w)):
            new_w[i] = w[i] + alpha * delta * f[i]
        return new_w

    # Shortest distance to exit
    def distance_to_exit(self, world, exit_location, grid):
        player = world.me(self)
        distance = 0
        vertical_diff = abs(exit_location[1] -  player.y)
        horizontal_diff = abs(exit_location[0] - player.x)
        distance = max(vertical_diff, horizontal_diff)
        # print("Player: ", player.y, player.x)
        # print("Exit: ", exit_location[1], exit_location[0])
        # distance = len(astar(grid, (player.y, player.x), (exit_location[1], exit_location[0])))
        # print("Distance: ", distance)

        return 1/distance

    #
    def distance_to_closest_monster(self, world, monsters, grid):
        if monsters:
            player = world.me(self)
            distance = max(world.width(), world.height())*2
            
            for monster in monsters:
                vertical_diff = abs(player.y - monster[1])
                horizontal_diff = abs(player.x - monster[0])
                diff = max(vertical_diff, horizontal_diff)

                # diff = len(astar(grid, (player.y, player.x), (monster[1], monster[0])))
                if diff < distance:
                    distance = diff
            
            return 1/distance
        else:
            return 0

    #
    def angle_between_closest_monster_and_exit(self, world, exit_location, monsters, grid):
        if monsters:
            player = world.me(self)
            distance = max(world.width(), world.height())*2
            closest_monster = (world.height(), world.width())

            for monster in monsters:
                vertical_diff = abs(player.y - monster[1])
                horizontal_diff = abs(player.x - monster[0])
                diff = max(vertical_diff, horizontal_diff)

                # diff = len(astar(grid, (player.y, player.x), (monster[1], monster[0])))
                if diff < distance:
                    distance = diff
                    closest_monster = (monster[1], monster[0])

            player_to_monster = np.array([closest_monster[0]-player.x, closest_monster[1]-player.y])
            player_to_exit = np.array([exit_location[0]-player.x, exit_location[1]-player.y])
            dot_product = np.dot(player_to_monster, player_to_exit)
            return 1/abs(math.degrees(math.acos(dot_product/((np.linalg.norm(player_to_monster)*(np.linalg.norm(player_to_exit)))))))

        else:
            return 0

    #
    def timer_of_closest_bomb(self, world, bombs, grid):
        if bombs:
            player = world.me(self)
            distance = max(world.width(), world.height())*2
            closest_bomb = (world.height(), world.width())
            
            for bomb in bombs:
                vertical_diff = abs(player.y - bomb.y)
                horizontal_diff = abs(player.x - bomb.x)
                diff = max(vertical_diff, horizontal_diff)

                # diff = len(astar(grid, (player.y, player.x), (bomb.y, bomb.x)))

                if diff < distance:
                    distance = diff
                    closest_bomb = (bomb.y, bomb.x)
            
            return world.bomb_at(closest_bomb[1], closest_bomb[0]).timer
        else:
            return 0
    
    def distance_to_closest_bomb(self, world, bombs, grid):
        if bombs:
            player = world.me(self)
            distance = max(world.width(), world.height())*2
            
            for bomb in bombs:
                vertical_diff = abs(player.y - bomb.y)
                horizontal_diff = abs(player.x - bomb.x)
                diff = max(vertical_diff, horizontal_diff)

                # diff = len(astar(grid, (player.y, player.x), (bomb.y, bomb.x)))
                if diff < distance:
                    distance = diff
            
            return 1/distance
        else:
            return 0
        
    #
    def distance_to_explosion(self, world, explosions, grid):
        if explosions:
            player = world.me(self)
            distance = max(world.width(), world.height())*2
            
            for explosion in explosions:
                vertical_diff = abs(player.y - explosion[1])
                horizontal_diff = abs(player.x - explosion[0])
                diff = max(vertical_diff, horizontal_diff)

                # diff = len(astar(grid, (player.y, player.x), (explosion[1], explosion[0])))
                if diff < distance:
                    distance = diff
            
            return 1/distance
        else:
            return 0

    #
    def distance_to_closest_wall(self, world, walls, grid):
        if walls:
            player = world.me(self)
            distance = max(world.width(), world.height())*2
            
            for wall in walls:
                vertical_diff = abs(player.y - wall[1])
                horizontal_diff = abs(player.x - wall[0])
                diff = max(vertical_diff, horizontal_diff)

                # diff = len(astar(grid, (player.y, player.x), (wall[1], wall[0])))
                if diff < distance:
                    distance = diff
            
            return 1/distance
        else:
            return 0

    #
    def distance_to_closest_character(self, world, characters, grid):
        if len(characters) > 1:
            player = world.me(self)
            distance = max(world.width(), world.height())*2
            
            for character in characters:
                if character != player:
                    vertical_diff = abs(player.y - character.y)
                    horizontal_diff = abs(player.x - character.x)
                    diff = max(vertical_diff, horizontal_diff)

                    # diff = len(astar(grid, (player.y, player.x), (character.y, character.x)))

                    if diff < distance:
                        distance = diff
            
            return 1/distance
        else:
            return 0

    def get_world_grid(self, world):
        # 2D world initially with zeros
        world_grid = np.zeros((world.height(), world.width()))

        # map out in 2D world grid where the walls are
        for row in range(world.height()):
            for col in range(world.width()):
                if world.wall_at(col, row) or world.bomb_at(col, row) or world.explosion_at(col, row):
                    world_grid[row][col] = 1
                elif world.monsters_at(col, row) or world.characters_at(col, row):
                    world_grid[row][col] = 1

        return world_grid


# A* Algorithm
# Author: Nicholas Swift
# code source: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


# maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#
# start = (0, 0)
# end = (7, 6)
#
# path = astar(maze, start, end)
# print(path)
# print(len(path))
