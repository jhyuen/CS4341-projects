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
        utilityVec = np.zeros(9)  # vector of zeros
        policyVec = np.zeros(9)  # vector of random policy

        unchanged = True
        while unchanged:
            utilityVec = self.policy_eval()
            unchanged = True
            for s in mdp.S:
                if ():
                    policyVec = 0
                    unchanged = False

        return policyVec



    def policy_eval(self):
        pass


class mdp():
    def __init__(self,states, actions, transition_model):
        self.states = states
        self.actions = actions
        self.transition_model = transition_model

    def get_states():
        return self.states

    def get_actions():
        return self.actions

    def get_transition_model():
        return self.transition_model




    

