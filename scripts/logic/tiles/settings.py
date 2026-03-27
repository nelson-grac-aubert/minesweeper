import pygame
import os

from scripts.logic.utils.assets_imports import load_image

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
DARKGREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BGCOLOUR = DARKGREY

# Game settings
TILESIZE = 32
ROWS = 15
COLS = 15
WIDTH = TILESIZE * ROWS
HEIGHT = TILESIZE * COLS
FPS = 60
TITLE = "MicrotransacMines"

DIFFICULTY_PARAMS = {
    "easy":   {"grid": 8,  "bombs_min": 6,  "bombs_max": 10},
    "medium": {"grid": 10, "bombs_min": 10,  "bombs_max": 15},
    "hard":   {"grid": 12, "bombs_min": 25, "bombs_max": 30},
}

DIFFICULTIES = {
    "facile": {
        "time_limit": 180
    },
    "normal": {
        "time_limit": 120
    },
    "pay": {
        "time_limit": 90
    }
}

tile_numbers = []
for i in range(1, 9):
    tile_numbers.append(pygame.transform.scale(pygame.image.load(os.path.join("assets\images", f"revealed_tile_{i}.png")), (TILESIZE, TILESIZE)))

tile_empty = pygame.transform.scale(pygame.image.load(os.path.join("assets\images", "revealed_tile.png")), (TILESIZE, TILESIZE))
tile_exploded = pygame.transform.scale(pygame.image.load(os.path.join("assets\images", "TileExploded.png")), (TILESIZE, TILESIZE))
tile_flag = pygame.transform.scale(pygame.image.load(os.path.join("assets\images", "masked_tile_flag.png")), (TILESIZE, TILESIZE))
tile_mine = pygame.transform.scale(pygame.image.load(os.path.join("assets\images", "revealed_tile_bomb.png")), (TILESIZE, TILESIZE))
tile_unknown = pygame.transform.scale(pygame.image.load(os.path.join("assets\images", "masked_tile.png")), (TILESIZE, TILESIZE))
tile_not_mine = pygame.transform.scale(pygame.image.load(os.path.join("assets\images", "TileNotMine.png")), (TILESIZE, TILESIZE))
tile_question_mark = pygame.transform.scale(pygame.image.load(os.path.join("assets\images", "masked_tile_question_mark.png")), (TILESIZE, TILESIZE))