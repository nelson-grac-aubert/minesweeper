# settings.py
import os
import pygame

# COLORS
WHITE     = (255, 255, 255)
BLACK     = (0, 0, 0)
DARKGREY  = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN     = (0, 255, 0)
DARKGREEN = (0, 200, 0)
BLUE      = (0, 0, 255)
RED       = (255, 0, 0)
YELLOW    = (255, 255, 0)
BGCOLOUR  = DARKGREY

# Game settings
TILESIZE = 32
FPS      = 60
TITLE    = "MicrotransacMines"

DIFFICULTIES = {
    "facile": {"rows": 9,  "cols": 9,  "min_mines": 5,  "max_mines": 10, "time_limit": 90},
    "normal": {"rows": 15, "cols": 15, "min_mines": 7,  "max_mines": 12, "time_limit": 60},
    "pay":    {"rows": 20, "cols": 20, "min_mines": 13, "max_mines": 30, "time_limit": 30},
}

# Images — toutes None jusqu'à l'appel de init_images()
tile_numbers      = []
tile_empty        = None
tile_exploded     = None
tile_flag         = None
tile_mine         = None
tile_unknown      = None
tile_not_mine     = None
tile_question_mark = None


def init_images(assets_dir):
    """
    Charge toutes les images du jeu.
    Doit être appelé après pygame.init(), en passant le chemin vers assets/images/.
    """
    global tile_numbers, tile_empty, tile_exploded, tile_flag
    global tile_mine, tile_unknown, tile_not_mine, tile_question_mark

    def load(filename):
        path = os.path.join(assets_dir, filename)
        return pygame.transform.scale(
            pygame.image.load(path).convert_alpha(), (TILESIZE, TILESIZE)
        )

    tile_numbers       = [load(f"revealed_tile_{i}.png") for i in range(1, 9)]
    tile_empty         = load("revealed_tile.png")
    tile_exploded      = load("TileExploded.png")
    tile_flag          = load("masked_tile_flag.png")
    tile_mine          = load("revealed_tile_bomb.png")
    tile_unknown       = load("masked_tile.png")
    tile_not_mine      = load("TileNotMine.png")
    tile_question_mark = load("masked_tile_question_mark.png")