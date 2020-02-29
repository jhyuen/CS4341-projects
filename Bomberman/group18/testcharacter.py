# This is necessary to find the main code
import sys
import numpy as np
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
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

