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
        "rows": 8,
        "cols": 8,
        "min_mines": 15,
        "max_mines": 17,
        "time_limit": 120
    },
    "normal": {
        "rows": 10,
        "cols": 10,
        "min_mines": 20,
        "max_mines": 22,
        "time_limit": 90
    },
    "pay": {
        "rows": 12,
        "cols": 12,
        "min_mines": 100,
        "max_mines": 110,
        "time_limit": 60
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