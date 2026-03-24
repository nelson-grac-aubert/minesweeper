import random
import pygame
from Tile_class import Tile
from settings import *

class Board:
    def __init__(self, rows, cols, amount_mines):
        self.rows = rows
        self.cols = cols
        self.amount_mines = amount_mines

        self.board_surface = pygame.Surface((cols * TILESIZE, rows * TILESIZE))

        self.board_list = [
            [Tile(col, row, tile_empty, ".") for row in range(self.rows)]
            for col in range(self.cols)
        ]

        self.place_mines()
        self.place_clues()
        self.dug = []

    def place_mines(self):
        for _ in range(self.amount_mines):
            while True:
                x = random.randint(0, self.cols - 1)
                y = random.randint(0, self.rows - 1)

                if self.board_list[x][y].type == ".":
                    self.board_list[x][y].image = tile_mine
                    self.board_list[x][y].type = "X"
                    break

    def place_clues(self):
        for x in range(self.cols):
            for y in range(self.rows):
                if self.board_list[x][y].type != "X":
                    total_mines = self.check_neighbours(x, y)
                    if total_mines > 0:
                        self.board_list[x][y].image = tile_numbers[total_mines - 1]
                        self.board_list[x][y].type = "C"

    def is_inside(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows

    def check_neighbours(self, x, y):
        total_mines = 0
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                neighbour_x = x + x_offset
                neighbour_y = y + y_offset

                if self.is_inside(neighbour_x, neighbour_y):
                    if self.board_list[neighbour_x][neighbour_y].type == "X":
                        total_mines += 1

        return total_mines

    def draw(self, screen):
        for row in self.board_list:
            for tile in row:
                tile.draw(self.board_surface)

        screen.blit(self.board_surface, (0, 0))

    def dig(self, x, y):
        self.dug.append((x, y))

        if self.board_list[x][y].type == "X":
            self.board_list[x][y].revealed = True
            self.board_list[x][y].image = tile_exploded
            return False

        elif self.board_list[x][y].type == "C":
            self.board_list[x][y].revealed = True
            return True

        self.board_list[x][y].revealed = True

        for row in range(max(0, x - 1), min(self.cols - 1, x + 1) + 1):
            for col in range(max(0, y - 1), min(self.rows - 1, y + 1) + 1):
                if (row, col) not in self.dug:
                    self.dig(row, col)

        return True

    def display_board(self):
        for row in self.board_list:
            print(row)