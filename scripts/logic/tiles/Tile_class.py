# A Tile that composes the game grid
# types list
# "." -> unknown
# "X" -> mine
# "C" -> clue
# "/" -> empty


import pygame
from settings import TILESIZE, tile_unknown, tile_flag, tile_question_mark

class Tile:
    """Represents a single tile in the Minesweeper grid."""
    def __init__(self, row, col, image, type, revealed=False, marker="none"):
        self.row = row
        self.col = col
        self.x = col * TILESIZE
        self.y = row * TILESIZE
        self.image = image
        self.type = type  # "." = unknown, "X" = mine, "C" = clue
        self.revealed = revealed
        self.marker = marker  # "none", "flag", "question"

    def toggle_marker(self):
        """Cycle marker: none → flag → question → none"""
        if self.marker == "none":
            self.marker = "flag"
        elif self.marker == "flag":
            self.marker = "question"
        elif self.marker == "question":
            self.marker = "none"

    def draw(self, screen):
        """Draw tile depending on revealed state or marker."""
        if self.revealed:
            screen.blit(self.image, (self.x, self.y))
        elif self.marker == "flag":
            screen.blit(tile_flag, (self.x, self.y))
        elif self.marker == "question":
            screen.blit(tile_question_mark, (self.x, self.y))
        else:
            screen.blit(tile_unknown, (self.x, self.y))

    def __repr__(self):
        return self.type