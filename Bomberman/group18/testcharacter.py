# This is necessary to find the main code
import sys
import numpy as np
import sensed_world as sw
import math
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back


class TestCharacter(CharacterEntity):

    def do(self, wrld):
        clone_world = wrld.from_world(wrld)
        clone_world.me(self).move(-1,-1)
        next_world = clone_world.next()[0]
        action = 1

        next_bombs = []
        next_explosions = []
        next_walls = []
        next_characters = []
        next_monsters = []
        next_exit_row = -1
        next_exit_col = -1

        print(self.x)
        print(self.y)
        
        for row in range(next_world.height()):
            for col in range(next_world.width()):
                if next_world.empty_at(col, row):
                    pass
                elif next_world.exit_at(col, row):
                    next_exit_row = row
                    next_exit_col = col
                elif next_world.wall_at(col, row):
                    next_walls.append((col,row))
                elif next_world.bomb_at(col, row):
                    next_bombs.append((col,row))
                elif next_world.explosion_at(col, row):
                    next_explosions.append((col,row))
                elif next_world.monsters_at(col, row):
                    next_monsters.append((col,row))
                elif next_world.characters_at(col, row):
                    next_characters.append((col,row))
        
        print('Factors')
        print('Distance to exit: ' + str(self.distance_to_exit(next_world, (next_exit_col, next_exit_row))))
        print('Distance to closest monster: ' + str(self.distance_to_closest_monster(next_world, next_monsters)))
        print('Angle between closest monster and exit: ' + str(self.angle_between_closest_monster_and_exit(next_world, (next_exit_col,next_exit_row), next_monsters)))
        print('Bomb Timer: ' + str(self.bomb_timer(next_world, next_bombs)))
        print('Distance to explosion: ' + str(self.distance_to_explosion(next_world, next_explosions)))
        print('Distance to wall: ' + str(self.distance_to_closest_wall(next_world, next_walls)))
        print('Distance to players: ' + str(self.distance_to_closest_character(next_world, next_characters)))

        '''
        chara_row, chara_col = 0, 0
        bomb = 0
        states = np.zeros((wrld.height(), wrld.width()))
        transition_model = []
        for row in range(wrld.height()):
            for col in range(wrld.width()):
                if wrld.empty_at(col, row):
                    states[row][col] = 0
                elif wrld.exit_at(col, row):
                    states[row][col] = 1
                elif wrld.wall_at(col, row):
                    states[row][col] = -1
                elif wrld.bomb_at(col, row):
                    states[row][col] = -1
                elif wrld.explosion_at(col, row):
                    states[row][col] = -1
                elif wrld.monsters_at(col, row):
                    states[row][col] = -1
                elif wrld.characters_at(col, row):
                    states[row][col] = -1
                    chara_row = row
                    chara_col = col

                transition_model.append(1)

        actions = [(-1, 1), (0, 1), (1, 1), (-1, 0), (0, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        # if actions[0]:
        #     dx -= 1
        #     dy += 1
        # elif actions[1]:
        #     dy += 1
        # elif actions[2]:
        #     dx += 1
        #     dy += 1
        # elif actions[3]:
        #     dx -= 1
        # elif actions[5]:
        #     dx += 1
        # elif actions[6]:
        #     dx -= 1
        #     dy -= 1
        # elif actions[7]:
        #     dy -= 1
        # elif actions[8]:
        #     dx += 1
        #     dy -= 1
        # else:
        #     bomb = 1

        # self.move(dx, dy)
        # if bomb:
        #     self.place_bomb()

        markovBaby = mdp(states, actions, transition_model)
        policy = self.policy_iteration(markovBaby, wrld)
        move = actions[policy[chara_row][chara_col]]
        print(policy)
        self.move(move[0], move[1])
        '''
        pass

    def policy_iteration(self, mdp, wrld):
        utility_vec = np.zeros((wrld.height(), wrld.width()))  # vector of zeros
        policy_vec = np.zeros((wrld.height(), wrld.width()))  # vector of random policy

        unchanged = True
        while unchanged:
            utility_vec = self.policy_eval(policy_vec, utility_vec, mdp, wrld)
            unchanged = True
            for col in range(wrld.width()):
                for row in range(wrld.height()):
                    # if probability of each action is 1
                    # if out of bound set utility to 0
                    next_states = np.zeros(9)

                    if row - 1 > 0:
                        next_states[1] = utility_vec[row-1][col]
                        if col - 1 > 0:
                            next_states[0] = utility_vec[row - 1][col - 1]
                            next_states[3] = utility_vec[row][col-1]
                        if col + 1 < wrld.width():
                            next_states[2] = utility_vec[row - 1][col + 1]
                            next_states[5] = utility_vec[row][col + 1]
                    if row + 1 < wrld.height():
                        next_states[7] = utility_vec[row + 1][col]
                        if col - 1 > 0:
                            next_states[3] = utility_vec[row][col - 1]
                            next_states[6] = utility_vec[row + 1][col - 1]
                        if col + 1 < wrld.width():
                            next_states[5] = utility_vec[row][col + 1]
                            next_states[8] = utility_vec[row + 1][col + 1]

                    max_utility = np.amax(next_states)
                    action = np.argmax(next_states)
                    policy_vec = policy_vec.astype(int)
                    if max_utility > next_states[policy_vec[row][col]]:
                        policy_vec[row][col] = action
                        unchanged = False

        return policy_vec

    def policy_eval(self, policy_vec, utility_vec, mdp, wrld):
        gamma = 0.95
        new_utility = np.zeros((wrld.height(), wrld.width()))
        policy_vec = policy_vec.astype(int)
        for col in range(wrld.width()):
            for row in range(wrld.height()):
                action = mdp.actions[policy_vec[row][col]]
                next_row = row + action[1]
                next_col = col + action[0]
                if 0 <= next_row < wrld.height() and 0 <= next_col < wrld.width():
                    new_utility[row][col] = mdp.states[next_row][next_col] + gamma*utility_vec[next_row][next_col]
        return new_utility

    # Shortest distance to exit - does not take walls into account
    def distance_to_exit(self, world, exit_location):
        player = world.me(self)
        distance = 0
        vertical_diff = abs(exit_location[1] -  player.y)
        horizontal_diff = abs(exit_location[0] - player.x)
        distance = max(vertical_diff,horizontal_diff)
        return 1/distance

    #
    def distance_to_closest_monster(self, world, monsters):
        if monsters:
            player = world.me(self)
            distance = max(world.width(),world.height())*2
            
            for monster in monsters:
                vertical_diff = abs(player.y - monster.y)
                horizontal_diff = abs(player.x - monster.x)
                diff = max(vertical_diff,horizontal_diff)
                if diff < distance:
                    distance = diff
            
            return 1/distance
        else:
            return 0

    #
    def angle_between_closest_monster_and_exit(self, world, exit_location, monsters):
        if monsters:
            player = world.me(self)
            distance = max(world.width(),world.height())*2
            closest_monster = (world.height(),world.width()) 

            for monster in monsters:
                vertical_diff = abs(player.y - monster.y)
                horizontal_diff = abs(player.x - monster.x)
                diff = max(vertical_diff,horizontal_diff)
                if diff < distance:
                    distance = diff
                    closest_monster = (monster.y, monster.x)

            player_to_monster = np.array([closest_monster[0]-player.x,closest_monster[1]-player.y])
            player_to_exit = np.array([exit_location[0]-player.x,exit_location[1]-player.y])
            dot_product = np.dot(player_to_monster, player_to_exit)
            return 1/abs(math.degrees(math.acos(dot_product/((np.linalg.norm(player_to_monster)*(np.linalg.norm(player_to_exit)))))))

        else:
            return 0

    #
    def timer_of_closest_bomb(self, world, bombs):
        if bombs:
            player = world.me(self)
            distance = max(world.width(),world.height())*2
            closest_bomb = (world.height(),world.width())
            
            for bomb in bombs:
                vertical_diff = abs(player.y - bomb.y)
                horizontal_diff = abs(player.x - bomb.x)
                diff = max(vertical_diff,horizontal_diff)
                if diff < distance:
                    distance = diff
                    closest_bomb = (bomb.y, bomb.x)
            
            return world.bomb_at(closest_bomb[1],closest_bomb[0]).timer
        else:
            return 0
    
    def distance_to_closest_bomb(self, world, bombs):
        if bombs:
            player = world.me(self)
            distance = max(world.width(),world.height())*2
            
            for bomb in bombs:
                vertical_diff = abs(player.y - bomb.y)
                horizontal_diff = abs(player.x - bomb.x)
                diff = max(vertical_diff,horizontal_diff)
                if diff < distance:
                    distance = diff
            
            return 1/distance
        else:
            return 0
        
    #
    def distance_to_explosion(self, world, explosions):
        if explosions:
            player = world.me(self)
            distance = max(world.width(),world.height())*2
            
            for explosion in explosions:
                vertical_diff = abs(player.y - explosion.y)
                horizontal_diff = abs(player.x - explosion.x)
                diff = max(vertical_diff,horizontal_diff)
                if diff < distance:
                    distance = diff
            
            return 1/distance
        else:
            return 0

    #
    def distance_to_closest_wall(self, world, walls):
        if walls:
            player = world.me(self)
            distance = max(world.width(),world.height())*2
            
            for wall in walls:
                vertical_diff = abs(player.y - wall.y)
                horizontal_diff = abs(player.x - wall.x)
                diff = max(vertical_diff,horizontal_diff)
                if diff < distance:
                    distance = diff
            
            return 1/distance
        else:
            return 0}

    #
    def distance_to_closest_character(self, world, characters):
        if characters.length() > 1:
            player = world.me(self)
            distance = max(world.width(),world.height())*2
            
            for character in characters:
                if character != player:
                    vertical_diff = abs(player.y - character.y)
                    horizontal_diff = abs(player.x - character.x)
                    diff = max(vertical_diff,horizontal_diff)
                    
                    if diff < distance:
                        distance = diff
            
            return 1/distance
        else:
            return 0

class mdp():
    def __init__(self,states, actions, transition_model):
        self.states = states
        self.actions = actions
        self.transition_model = transition_model

    def get_states(self):
        return self.states

    def get_actions(self):
        return self.actions

    def get_transition_model(self):
        return self.transition_model






