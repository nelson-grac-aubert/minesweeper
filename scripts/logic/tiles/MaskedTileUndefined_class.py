# The masked tile that composes all of the board on turn 1
# It is never a bomb, so the player never loses on turn 1 
# It generates all the other tiles as MaskedSafe or MaskedBombs, then reveals itself (and maybe its neigbours)

from MaskedTile_class import MaskedTile

class MaskedTileSafe(MaskedTile) : 
    pass