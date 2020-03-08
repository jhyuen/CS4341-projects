# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster

# TODO This is your code!
sys.path.insert(1, '../groupNN')
# from Qcharacter import QCharacter
from interactivecharacter import InteractiveCharacter

# Create the game
random.seed(1000) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(StupidMonster("stupid", # name
                            "S",      # avatar
                            3, 9      # position
))



# TODO Add your character
# g.add_character(chara("me", # name
#                               "C",  # avatar
#                               0, 0  # position
# ))

g.add_character(InteractiveCharacter("me", # name
                                   "C",  # avatar
                                   0, 0  # position
))

# chara = QCharacter("me", "C", 0, 0)
# chara.setFilename("../variant2.txt")
# g.add_character(chara)

# Run!
g.go(1)
