# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../group18')
# from testcharacter import TestCharacter
from Qcharacter import QCharacter

# Create the game
random.seed(100) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(StupidMonster("stupid", # name
                            "S",      # avatar
                            3, 5,     # position
))
g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    3, 13,        # position
                                    2             # detection range
))

# TODO Add your character
# g.add_character(TestCharacter("me", # name
#                               "C",  # avatar
#                               0, 0  # position
# ))

chara = QCharacter("me", "C", 0, 0)
chara.setFilename("../scenario2_variant5.txt")
g.add_character(chara)

# Run!
g.go()
