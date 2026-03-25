# maps/heart/board.py
# Carte en forme de cœur.
 
import random
import sys
import os
import pygame
 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import settings
from settings import TILESIZE, BGCOLOUR
from Tile_class import Tile
 
ROWS = 18
COLS = 20
 
 
def _is_heart(row, col):
    """
    Retourne True si (row, col) appartient à la forme cœur.
    Deux lobes circulaires (haut) + triangle (bas).
    """
    x = (col - COLS / 2 + 0.5) / (COLS / 2)
    y = (row / ROWS) * 2 - 1           # -1 = haut, +1 = bas
 
    lobe_gauche = (x + 0.5) ** 2 + (y + 0.3) ** 2 < 0.32
    lobe_droit  = (x - 0.5) ** 2 + (y + 0.3) ** 2 < 0.32
    triangle    = abs(x) < (1 - y) * 0.75 and y > -0.35
 
    return lobe_gauche or lobe_droit or triangle
 
 
class Board:
    """Grille en forme de cœur."""
 
    def __init__(self, rows, cols, amount_mines):
        self.rows         = ROWS          # dimensions fixes pour le cœur
        self.cols         = COLS
        self.amount_mines = amount_mines
        self.board_list   = [[Tile(r, c, ".") for c in range(COLS)] for r in range(ROWS)]
        self.dug          = []
        self.mines_placed = False
 
        # Marque les cases hors cœur
        self._playable = set()
        for r in range(ROWS):
            for c in range(COLS):
                if _is_heart(r, c):
                    self._playable.add((r, c))
                else:
                    self.board_list[r][c].type = "N"
 
        self._surface = pygame.Surface((COLS * TILESIZE, ROWS * TILESIZE))
 
    # setup
 
    def place_mines(self, safe_row, safe_col):
        """Place mines dans le cœur en évitant la case cliquée et ses voisines."""
        safe = {
            (safe_row + dr, safe_col + dc)
            for dr in range(-1, 2)
            for dc in range(-1, 2)
            if (safe_row + dr, safe_col + dc) in self._playable
        }
        candidates = list(self._playable - safe)
        for r, c in random.sample(candidates, self.amount_mines):
            self.board_list[r][c].type = "X"
 
        self.place_clues()
        self.mines_placed = True
 
    def place_clues(self):
        """Assigne les chiffres aux cases du cœur adjacentes aux mines."""
        for r, c in self._playable:
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
                if (r, c) in self._playable and self.board_list[r][c].type == "X":
                    total += 1
        return total
 
    # dig (récursif)
 
    def dig(self, row, col):
        """
        Révèle la case (row, col) récursivement.
        Retourne False si mine touchée, True sinon.
 
        Cas de base  : déjà visité / hors cœur / indice / mine
        Cas récursif : case vide → propage aux 8 voisins dans le cœur
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
 
        # Case vide → révèle et propage aux 8 voisins dans le cœur
        tile.revealed = True
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = row + dr, col + dc
                if (r, c) in self._playable and (r, c) not in self.dug:
                    self.dig(r, c)
 
        return True
 
    def reveal_all_mines(self):
        for r, c in self._playable:
            if self.board_list[r][c].type == "X":
                self.board_list[r][c].revealed = True
 
    def check_win(self):
        for r, c in self._playable:
            tile = self.board_list[r][c]
            if tile.type != "X" and not tile.revealed:
                return False
        return True
 
    def is_playable(self, row, col):
        return (row, col) in self._playable
 
    #  draw
 
    def draw(self, screen):
        self._surface.fill(BGCOLOUR)
        for row in self.board_list:
            for tile in row:
                tile.draw(self._surface)
        screen.blit(self._surface, (0, 0))