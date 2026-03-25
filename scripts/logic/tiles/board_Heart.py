import random
from scripts.logic.tiles.Tile_class import Tile
from scripts.logic.tiles.settings import (
    tile_unknown, tile_empty, tile_mine,
    tile_numbers, tile_exploded, tile_not_mine, TILESIZE
)

HEART_PATTERN = [
    "  ***   ***  ",
    " ***** ***** ",
    "*************",
    " *********** ",
    "  *********  ",
    "   *******   ",
    "    *****    ",
    "     ***     ",
    "      *      ",
]

HEART_ROWS = len(HEART_PATTERN)
HEART_COLS = max(len(row) for row in HEART_PATTERN)


class Board_Heart:
    """Grille jouable en forme de cœur — sans héritage de Board."""

    def __init__(self, amount_mines: int):
        self.rows         = HEART_ROWS
        self.cols         = HEART_COLS
        self.amount_mines = amount_mines
        self.mines_placed = False
        self.dug          = []
        self.board_list   = self._build_grid()
        self._void        = self._collect_void()

    # ── construction ────────────────────────────────────────────────────────

    def _build_grid(self):
        grid = []
        for r in range(HEART_ROWS):
            row_tiles = []
            for c in range(HEART_COLS):
                pat = HEART_PATTERN[r]
                if c < len(pat) and pat[c] == "*":
                    row_tiles.append(Tile(r, c, tile_unknown, "."))
                else:
                    row_tiles.append(Tile(r, c, tile_empty, "/", revealed=True))
            grid.append(row_tiles)
        return grid

    def _collect_void(self):
        return {
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if self.board_list[r][c].type == "/"
        }

    # ── placement ───────────────────────────────────────────────────────────

    def place_mines(self, safe_row: int, safe_col: int):
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
            and (r, c) not in self._void
            and self.board_list[r][c].type == "."
        ]
        count = min(self.amount_mines, len(candidates))
        for r, c in random.sample(candidates, count):
            self.board_list[r][c].type  = "X"
            self.board_list[r][c].image = tile_mine

        self._place_clues()
        self.mines_placed = True

    def _place_clues(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board_list[r][c].type in ("X", "/"):
                    continue
                adj = sum(
                    1
                    for dr in range(-1, 2)
                    for dc in range(-1, 2)
                    if (dr, dc) != (0, 0)
                    and 0 <= r + dr < self.rows
                    and 0 <= c + dc < self.cols
                    and self.board_list[r + dr][c + dc].type == "X"
                )
                if adj > 0:
                    self.board_list[r][c].type  = "C"
                    self.board_list[r][c].image = tile_numbers[adj - 1]

    # ── dig ─────────────────────────────────────────────────────────────────

    def dig(self, row: int, col: int):
        if (row, col) in self._void:
            return True
        self.dug.append((row, col))
        tile = self.board_list[row][col]

        if tile.type == "X":
            tile.revealed = True
            tile.image    = tile_exploded
            return False
        if tile.type == "C":
            tile.revealed = True
            return True

        tile.revealed = True
        tile.image    = tile_empty
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = row + dr, col + dc
                if (dr, dc) != (0, 0) \
                   and 0 <= r < self.rows \
                   and 0 <= c < self.cols \
                   and (r, c) not in self.dug \
                   and (r, c) not in self._void:
                    self.dig(r, c)
        return True

    def reveal_all_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board_list[r][c].type == "X":
                    self.board_list[r][c].revealed = True

    def check_win(self) -> bool:
        return all(
            self.board_list[r][c].revealed
            for r in range(self.rows)
            for c in range(self.cols)
            if self.board_list[r][c].type not in ("X", "/")
        )

    def draw(self, screen):
        for row in self.board_list:
            for tile in row:
                tile.draw(screen)