# COLORS (r, g, b)
import pygame
import os

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

# game settings
TILESIZE = 32
ROWS = 15
COLS = 15
AMOUNT_MINES = 5
WIDTH = TILESIZE * ROWS
HEIGHT = TILESIZE * COLS
FPS = 60
TITLE = "MicrotransacMines"

DIFFICULTIES = {
    "facile": {
        "rows": 10,
        "cols": 10,
        "min_mines": 0,
        "max_mines": 6,
        "time_limit": 90
    },
    "normal": {
        "rows": 15,
        "cols": 15,
        "min_mines": 7,
        "max_mines": 12,
        "time_limit": 60
    },
    "pay": {
        "rows": 20,
        "cols": 20,
        "min_mines": 13,
        "max_mines": 30,
        "time_limit": 30
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