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

    player_last_x = -1
    player_last_y = -1

    filename = ""

    def setFilename(self, filename):
        self.filename = filename

    def do(self, wrld):
        # read w from file
        f = open(self.filename, 'r')
        w = list(map(float, f.read().split(" ")))
        f.close()

        next_exit_row = 0
        next_exit_col = 0
        for row in range(wrld.height()):
            for col in range(wrld.width()):
                if wrld.exit_at(col, row):
                    next_exit_row = row
                    next_exit_col = col

        player = wrld.me(self)
        #(newwrld, events) = wrld.next()
        grid = self.get_world_grid(wrld)    # changed newwrld to wrld
        path = astar(grid, (player.y, player.x), (next_exit_row, next_exit_col))
        exit_dis = len(path)
        print('Path: ' + str(path))
        print("Exit Distance: ", exit_dis)

        # stores optimal action list
        actlist = self.optiact(wrld, w, exit_dis, path)

        print("Action did take: ", actlist[0],  ", ", actlist[1])
        print("Bomb?: ", actlist[2])
        self.move(actlist[0], actlist[1])
        if actlist[2]:
            self.place_bomb()

        (updatedwrld, events) = wrld.next()

        # TODO: check if the game has ended (done() function)

        # calculate rewards for the action
        print("event list", actlist[5])
        r = self.reward(actlist[4], events)

        print("Q Learning Values: ")
        new_w = self.Qlearning(updatedwrld, events, actlist[3], actlist[6], r, w, exit_dis, path)

        # write to file
        f = open(self.filename, "w")
        f.write(' '.join(str(x) for x in new_w))
        f.close()
        pass


    # given a world configuration, returns a list for optimal actions and highest Q value
    # in order of [dx, dy, bomb?, Q, newwrld, events, function values]
    def optiact(self, wrld, w, exit_dis, path):
        #
        # Get first character in the world
        m = wrld.me(self)

        # keep track of highest Q value so far
        Q = -math.inf

        # stores best move for the character, in order of [dx, dy, bomb?, maxQ, newwrld, events]
        # default value moves toward down right and places the bomb
        # TODO: reset default value or figure out better way to initialize values
        action = [0, 0, False, Q, wrld.next(), [], []]

        # Go through the possible 8-moves of the character and placing the bomb
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

                                print('Events before the world ends: ')
                                for event in events:
                                    print(event)
                                    print(event.tpe)

                                if self.is_world_ended(events):
                                    print("THE WORLD HAS ENDED")
                                    Q = 0
                                    action[0] = dx
                                    action[1] = dy
                                    action[2] = False
                                    action[3] = Q
                                    action[4] = wrld
                                    action[5] = []

                                    newQ = self.approxQ(newwrld, dx, dy, False, w, exit_dis, path)
                                    action[6] = newQ[1]
                                else:
                                    # calculate approximate Q value for the new world state
                                    newQ = self.approxQ(newwrld, dx, dy, False, w, exit_dis, path)
                                    # if new Q value is greater than previous, update optimal actions
                                    if newQ[0] > Q:
                                        Q = newQ[0]
                                        action[0] = dx
                                        action[1] = dy
                                        action[2] = False
                                        action[3] = newQ[0]
                                        action[4] = newwrld
                                        action[5] = events
                                        action[6] = newQ[1]
                    if dx == 0 and dy == 0:
                        # Set move in wrld
                        m.move(dx, dy)
                        self.place_bomb()
                        # Get new world
                        (newwrld, events) = wrld.next()
                        
                        if self.is_world_ended(events):
                            Q = 0
                            action[0] = dx
                            action[1] = dy
                            action[2] = False
                            action[3] = Q
                            action[4] = wrld
                            action[5] = []

                            newQ = self.approxQ(newwrld, dx, dy, True, w, exit_dis, path)
                            action[6] = newQ[1]
                        else:
                            # calculate approximate Q value for the new world state
                            newQ = self.approxQ(newwrld, dx, dy, True, w, exit_dis, path)
                            # if new Q value is greater than previous, update optimal actions
                            if newQ[0] > Q:
                                Q = newQ[0]
                                action[0] = dx
                                action[1] = dy
                                action[2] = True
                                action[3] = newQ[0]
                                action[4] = newwrld
                                action[5] = events
                                action[6] = newQ[1]
        return action



    # returns score for certain character given a world and events
    # TODO: finish defining reward function
    def reward(self, wrld, events):
        r = 0

        for e in events:
            if e.tpe == Event.BOMB_HIT_WALL:
                r += 0.5
            elif e.tpe == Event.BOMB_HIT_MONSTER:
                r += 1
            elif e.tpe == Event.CHARACTER_KILLED_BY_MONSTER:    
                r -= 2
            elif e.tpe == Event.BOMB_HIT_CHARACTER:
                r -= 2
            elif e.tpe == Event.CHARACTER_FOUND_EXIT:
                r += 2

        if not self.is_world_ended(events):
            r += 0.01

        return r

    # returns approximate Q value given a world state and the actions the character took
    # TODO: finish calculating approximate Q value
    def approxQ(self, wrld, dx, dy, bomb, w, exit_dis, path):
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

        player = wrld.me(self)
        if player:
            self.player_last_x = player.x
            self.player_last_y = player.y
        else:
            self.player_last_x += dx
            self.player_last_y += dy

        f.append(self.distance_to_path(wrld, exit_dis, path, self.player_last_x, self.player_last_y))
        f.append(self.distance_to_closest_monster(wrld, next_monsters, self.player_last_x, self.player_last_y))
        #f.append(self.angle_between_closest_monster_and_exit(wrld, (next_exit_col, next_exit_row), next_monsters, player_last_x, player_last_y))
        #f.append(self.timer_of_closest_bomb(wrld, next_bombs, player_last_x, player_last_y))
        f.append(self.distance_to_closest_bomb(wrld, next_bombs, self.player_last_x, self.player_last_y))
        f.append(self.distance_to_explosion(wrld, next_explosions, self.player_last_x, self.player_last_y))
        #f.append(self.distance_to_closest_wall(wrld, next_walls, player_last_x, player_last_y))
        #f.append(self.distance_to_closest_character(wrld, next_characters))
        
        Q = 0
        for i in range(0, len(w)):
            Q += w[i]*f[i]

        print("dx, dy: ", dx, dy)
        print("Q Value: ", Q)
        print("f values: ")
        print(f)
        return Q, f

    # updates w values after each action
    def Qlearning(self, updated_world, events, Q, f, r, w, exit_dis, path):
        alpha = 0.95
        gamma = 0.9

        print("Reward: ", r)
        # update w values
        if self.is_world_ended(events):
            delta = (r + gamma * 0) - Q
        else:
            delta = (r + gamma * self.optiact(updated_world, w, exit_dis, path)[3]) - Q
        print("delta: ", delta)
        new_w = np.zeros(len(w))
        print('w',w)
        print('f',f)
        for i in range(len(w)):
            new_w[i] = w[i] + alpha * delta * f[i]
        return new_w

    # Shortest distance to exit

    def distance_to_path(self, world, exit_dis, path, player_x, player_y):
        # player = world.me(self)
        dis_from_path = math.inf
        new_exit_dis = -1

        for i,coord in enumerate(path):
            # calculate how many moves to reach path
            # overwrite current dis_from_path if the number of moves is <= to 
            # find the coordinates of the closest move
            if max(abs(player_y - coord[0]),abs(player_x - coord[1])) <= dis_from_path: 
                dis_from_path = max(abs(player_y - coord[0]),abs(player_x - coord[1]))
                # closestCoordToPath = (coord[1], coord[0]) # (col, row) as opposed to former
                new_exit_dis = len(path)-i

        print("Player: ", player_y, player_x)
        print("path dis: ", dis_from_path)
        print('new_exit_dis: ', new_exit_dis)

        return 1/(new_exit_dis + dis_from_path + 1)


    def distance_to_closest_monster(self, world, monsters, player_x, player_y):
        if monsters:
            # player = world.me(self)
            distance = max(world.width(), world.height())*2
            
            for monster in monsters:
                vertical_diff = abs(player_y - monster[1])
                horizontal_diff = abs(player_x - monster[0])
                diff = max(vertical_diff, horizontal_diff)

                if diff < distance:
                    distance = diff
            
            return distance
        else:
            return 0

    #
    def angle_between_closest_monster_and_exit(self, world, exit_location, monsters, player_x, player_y):
        if monsters:
            # player = world.me(self)
            distance = max(world.width(), world.height())*2
            closest_monster = (world.height(), world.width())

            for monster in monsters:
                vertical_diff = abs(player_y - monster[1])
                horizontal_diff = abs(player_x - monster[0])
                diff = max(vertical_diff, horizontal_diff)

                if diff < distance:
                    distance = diff
                    closest_monster = (monster[0], monster[1])

            player_to_monster = np.array([closest_monster[0]-player_x, closest_monster[1]-player_y])
            player_to_exit = np.array([exit_location[0]-player_x, exit_location[1]-player_y])
            dot_product = np.dot(player_to_monster, player_to_exit)
            return 1/abs(math.degrees(math.acos(dot_product/((np.linalg.norm(player_to_monster)*(np.linalg.norm(player_to_exit)))))))

        else:
            return 0

    #
    def timer_of_closest_bomb(self, world, bombs, player_x, player_y):
        if bombs:
            # player = world.me(self)
            distance = max(world.width(), world.height())*2
            closest_bomb = (world.height(), world.width())
            
            for bomb in bombs:
                vertical_diff = abs(player_y - bomb[1])
                horizontal_diff = abs(player_x - bomb[0])
                diff = max(vertical_diff, horizontal_diff)

                if diff < distance:
                    distance = diff
                    closest_bomb = (bomb[0], bomb[1])
            
            return world.bomb_at(closest_bomb[0], closest_bomb[1]).timer
        else:
            return 0
    
    def distance_to_closest_bomb(self, world, bombs, player_x, player_y):
        if bombs:
            # player = world.me(self)
            distance = max(world.width(), world.height())*2
            
            for bomb in bombs:
                vertical_diff = abs(player_y - bomb[1])
                horizontal_diff = abs(player_x - bomb[0])
                diff = max(vertical_diff, horizontal_diff)

                if diff < distance:
                    distance = diff
            
            return distance
        else:
            return 0
        
    #
    def distance_to_explosion(self, world, explosions, player_x, player_y):
        if explosions:
            # player = world.me(self)
            distance = max(world.width(), world.height())*2
            
            for explosion in explosions:
                vertical_diff = abs(player_y - explosion[1])
                horizontal_diff = abs(player_x - explosion[0])
                diff = max(vertical_diff, horizontal_diff)

                if diff < distance:
                    distance = diff
            
            return distance
        else:
            return 0

    #
    def distance_to_closest_wall(self, world, walls, player_x, player_y):
        if walls:
            # player = world.me(self)
            distance = max(world.width(), world.height())*2
            
            for wall in walls:
                vertical_diff = abs(player_y - wall[1])
                horizontal_diff = abs(player_x - wall[0])
                diff = max(vertical_diff, horizontal_diff)

                if diff < distance:
                    distance = diff
            
            return 1/(distance+1)
        else:
            return 0

    #
    def distance_to_closest_character(self, world, characters):
        player = world.me(self)

        if len(characters) > 1 and player:
            distance = max(world.width(), world.height())*2
            
            for character in characters:
                if character != player:
                    vertical_diff = abs(player.y - character[1])
                    horizontal_diff = abs(player.x - character[0])
                    diff = max(vertical_diff, horizontal_diff)

                    if diff < distance:
                        distance = diff
            
            return 1/(distance+1)
        else:
            return 0

    def get_world_grid(self, world):
        # 2D world initially with zeros
        world_grid = np.zeros((world.height(), world.width()))

        # map out in 2D world grid where the walls are
        for row in range(world.height()):
            for col in range(world.width()):
                if world.wall_at(col, row):
                    world_grid[row][col] = 1
                

        return world_grid

    def is_world_ended(self, events):
        for event in events:
            if event.tpe == Event.BOMB_HIT_CHARACTER:
                return True
            elif event.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                return True
            elif event.tpe == Event.CHARACTER_FOUND_EXIT:
                return True
        return False


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
    def __hash__(self):
        return hash(self.position)

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = set()

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
        closed_list.add(current_node)

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
            if child in closed_list:
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



