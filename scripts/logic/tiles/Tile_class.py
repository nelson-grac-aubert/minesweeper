# Tile_class.py
# types list:
# "." -> unknown/empty
# "X" -> mine
# "C" -> clue
# "N" -> hors forme (non jouable)
 
import pygame
import settings
from settings import TILESIZE
 
 
class Tile:
    """Represents a single tile in the Minesweeper grid."""
 
    def __init__(self, row, col, type, revealed=False, marker="none"):
        self.row      = row
        self.col      = col
        self.x        = col * TILESIZE
        self.y        = row * TILESIZE
        self.type     = type   # "." | "X" | "C" | "N"
        self.revealed = revealed
        self.marker   = marker  # "none" | "flag" | "question"
 
    def toggle_marker(self):
        """Cycle marker: none → flag → question → none"""
        if self.marker == "none":
            self.marker = "flag"
        elif self.marker == "flag":
            self.marker = "question"
        else:
            self.marker = "none"
 
    def draw(self, screen):
        """Draw tile depending on revealed state or marker."""
        if self.type == "N":
            return  # hors forme → invisible
 
        if self.revealed:
            if self.type == "X":
                screen.blit(settings.tile_mine,    (self.x, self.y))
            elif self.type == "C":
                screen.blit(self.image,            (self.x, self.y))
            else:
                screen.blit(settings.tile_empty,   (self.x, self.y))
        elif self.marker == "flag":
            screen.blit(settings.tile_flag,        (self.x, self.y))
        elif self.marker == "question":
            screen.blit(settings.tile_question_mark, (self.x, self.y))
        else:
            screen.blit(settings.tile_unknown,     (self.x, self.y))
 
    def __repr__(self):
        return self.type