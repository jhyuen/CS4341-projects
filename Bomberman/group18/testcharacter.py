# This is necessary to find the main code
import sys
import numpy as np
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        
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






