# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../group18')
from Qcharacter import QCharacter


# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character
# g.add_character(TestCharacter("me", # name
#                               "C",  # avatar
#                               0, 0  # position
# ))

chara = QCharacter("me", "C", 0, 0)
chara.setFilename("../scenario2_variant1.txt")
g.add_character(chara)

# Run!
g.go(1)
