# This is necessary to find the main code
import sys
import numpy as np
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        
        dx, dy = 0, 0
        bomb = 0
        states = []
        transition_model = []
        for x in range(0,wrld.width()):
            for y in range(0,wrld.height()):
                if wrld.empty_at(x,y):
                    states.append(0)
                elif wrld.exit_at(x, y):
                    states.append(1)
                elif wrld.wall_at(x,y):
                    states.append(2)
                elif wrld.bomb_at(x,y):
                    states.append(3)
                elif wrld.explosion_at(x,y):
                    states.append(4)
                elif wrld.monsters_at(x,y):
                    states.append(5)
                elif wrld.characters_at(x,y):
                    states.append(6)

                transition_model.append(1)

        actions = [1,1,1,1,1,1,1,1,1]
        if actions[0]:
            dx -= 1
            dy += 1
        elif actions[1]:
            dy += 1
        elif actions[2]:
            dx += 1
            dy += 1
        elif actions[3]:
            dx -= 1
        elif actions[5]:
            dx += 1
        elif actions[6]:
            dx -= 1
            dy -= 1
        elif actions[7]:
            dy -= 1
        elif actions[8]:
            dx += 1
            dy -= 1
        else:
            bomb = 1

        self.move(dx, dy)
        if bomb:
            self.place_bomb()

        markovBaby = mdp(states,actions,transition_model)
        pass

    def policy_iteration(self, mdp):
        utility_vec = np.zeros(9)  # vector of zeros
        policy_vec = np.zeros(9)  # vector of random policy

        unchanged = True
        while unchanged:
            utility_vec = self.policy_eval(utility_vec, mdp)
            unchanged = True
            for s in range(mdp.S):
                # if probability of each action is 1
                top = utility_vec[s - width]
                bottom = utility_vec[s + width]
                right = utility_vec[s + 1]
                left = utility_vec[s - 1]
                top_right = utility_vec[s - width + 1]
                top_left = utility_vec[s - width - 1]
                bottom_right = utility_vec[s + width + 1]
                bottom_left = utility_vec[s + width - 1]

                next_states = np.array([top_left, top, top_right, left, right, bottom_left, bottom, bottom_right])
                max_utility = np.amax(next_states)
                action = np.argmax(next_states)

                if max_utility > utility_vec[next_states[policy_vec[s]]]:
                    policy_vec[s] = action
                    unchanged = False

        return policy_vec

    def policy_eval(self, utility_vec, mdp):
        return utility_vec

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






