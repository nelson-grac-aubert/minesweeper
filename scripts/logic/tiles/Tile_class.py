# A Tile that composes the game grid

import random
import pygame
from board import *
from settings import *

# types list
# "." -> unknown
# "X" -> mine
# "C" -> clue
# "/" -> empty


class Tile:
    def __init__(self, x, y, image, type, revealed=False, marker="none"):
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.image = image
        self.type = type
        self.revealed = revealed
        self.marker = marker  # "none", "flag", "question"

    def toggle_marker(self):
        """change none -> flag -> question -> none"""
        if self.marker == "none":
            self.marker = "flag"
        elif self.marker == "flag":
            self.marker = "question"
        elif self.marker == "question":
            self.marker = "none"

    def draw(self, board_surface):
        if self.revealed:
            board_surface.blit(self.image, (self.x, self.y))
        elif self.marker == "flag":
            board_surface.blit(tile_flag, (self.x, self.y))
        elif self.marker == "question":
            board_surface.blit(tile_question_mark, (self.x, self.y))
        else:
            board_surface.blit(tile_unknown, (self.x, self.y))

    def __repr__(self):
        return self.type