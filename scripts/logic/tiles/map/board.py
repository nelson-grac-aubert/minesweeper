# maps/classic/board.py
# Carte classique : grille rectangulaire.

import random
import sys
import os
import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import settings
from settings import TILESIZE, BGCOLOUR
from Tile_class import Tile


class Board:
    """Grille rectangulaire classique."""

    def __init__(self, rows, cols, amount_mines):
        self.rows         = rows
        self.cols         = cols
        self.amount_mines = amount_mines
        self.board_list   = [[Tile(r, c, ".") for c in range(cols)] for r in range(rows)]
        self.dug          = []
        self.mines_placed = False

        self._surface = pygame.Surface((cols * TILESIZE, rows * TILESIZE))

    # ---------------------------------------------------------------- setup

    def place_mines(self, safe_row, safe_col):
        """Place mines en évitant la case cliquée et ses voisines."""
        safe = {
            (safe_row + dr, safe_col + dc)
            for dr in range(-1, 2)
            for dc in range(-1, 2)
            if 0 <= safe_row + dr < self.rows and 0 <= safe_col + dc < self.cols
        }
        candidates = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) not in safe
        ]
        for r, c in random.sample(candidates, self.amount_mines):
            self.board_list[r][c].type = "X"

        self.place_clues()
        self.mines_placed = True

    def place_clues(self):
        """Assigne les chiffres aux cases adjacentes aux mines."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board_list[r][c].type != "X":
                    count = self.count_adjacent_mines(r, c)
                    if count > 0:
                        self.board_list[r][c].type  = "C"
                        self.board_list[r][c].image = settings.tile_numbers[count - 1]

    def count_adjacent_mines(self, row, col):
        """Retourne le nombre de mines autour d'une case."""
        total = 0
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    if self.board_list[r][c].type == "X":
                        total += 1
        return total

    # ---------------------------------------------------------------- dig (récursif)

    def dig(self, row, col):
        """
        Révèle la case (row, col) récursivement.
        Retourne False si mine touchée, True sinon.

        Cas de base  : déjà visité / marqué / indice / mine
        Cas récursif : case vide → propage aux 8 voisins
        """
        self.dug.append((row, col))
        tile = self.board_list[row][col]

        # Mine → défaite
        if tile.type == "X":
            tile.revealed = True
            tile.image    = settings.tile_exploded
            return False

        # Indice → on révèle et on s'arrête
        if tile.type == "C":
            tile.revealed = True
            return True

        # Case vide → révèle et propage aux 8 voisins
        tile.revealed = True
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols and (r, c) not in self.dug:
                    self.dig(r, c)

        return True

    def reveal_all_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board_list[r][c].type == "X":
                    self.board_list[r][c].revealed = True

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                tile = self.board_list[r][c]
                if tile.type != "X" and not tile.revealed:
                    return False
        return True

    # ---------------------------------------------------------------- draw

    def draw(self, screen):
        self._surface.fill(BGCOLOUR)
        for row in self.board_list:
            for tile in row:
                tile.draw(self._surface)
        screen.blit(self._surface, (0, 0))