import random
from scripts.logic.tiles.Tile_class import Tile
from scripts.logic.tiles.settings import tile_unknown, tile_numbers, tile_mine, tile_exploded, tile_empty, TILESIZE

class Board:
    """Manages the Minesweeper grid, mine placement, and digging."""
    def __init__(self, rows, cols, amount_mines):
        self.rows = rows
        self.cols = cols
        self.amount_mines = amount_mines
        self.board_list = [[Tile(r, c, tile_unknown, ".") for c in range(cols)] for r in range(rows)]
        self.dug = []
        self.mines_placed = False  # Mines will be placed after first click

    def place_mines(self, safe_row, safe_col):
        """Place mines avoiding the first clicked tile AND all its neighbors.

        Guaranteeing the clicked cell has 0 adjacent mines means it will always
        be type "." after place_clues(), so dig() will always trigger the
        recursive flood-reveal on the first click.
        """
        safe_cells = set()
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = safe_row + dr, safe_col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    safe_cells.add((r, c))

        placed = 0
        while placed < self.amount_mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if (r, c) in safe_cells or self.board_list[r][c].type == "X":
                continue
            self.board_list[r][c].type = "X"
            self.board_list[r][c].image = tile_mine
            placed += 1
        self.place_clues()
        self.mines_placed = True

    def place_clues(self):
        """Assign numbers to tiles next to mines."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board_list[r][c].type != "X":
                    count = self.count_adjacent_mines(r, c)
                    if count > 0:
                        self.board_list[r][c].type = "C"
                        self.board_list[r][c].image = tile_numbers[count - 1]

    def count_adjacent_mines(self, row, col):
        """Return number of mines around a tile."""
        total = 0
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    if self.board_list[r][c].type == "X":
                        total += 1
        return total

    def dig(self, row, col):
        """Reveal a tile; recursively reveal empty tiles."""
        self.dug.append((row, col))
        tile = self.board_list[row][col]
        if tile.type == "X":
            tile.revealed = True
            tile.image = tile_exploded
            return False
        elif tile.type == "C":
            tile.revealed = True
            return True

        tile.image = tile_empty
        tile.revealed = True
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols and (r, c) not in self.dug:
                    self.dig(r, c)
        return True

    def check_win(self):
        """Return True when every non-mine tile has been revealed."""
        for row in self.board_list:
            for tile in row:
                if tile.type != "X" and not tile.revealed:
                    return False
        return True

    def draw(self, screen):
        """Draw all tiles on the screen."""
        for row in self.board_list:
            for tile in row:
                tile.draw(screen)