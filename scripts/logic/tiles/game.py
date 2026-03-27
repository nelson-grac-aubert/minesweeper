import pygame
pygame.init()
import random

from scripts.logic.tiles.settings import (
    DIFFICULTIES, TILESIZE, FPS, BGCOLOUR, WHITE, RED, TITLE, tile_not_mine
)
from scripts.logic.tiles.board import Board
from scripts.logic.tiles.board_Heart import Board_Heart, HEART_ROWS, HEART_COLS

MAP_MODES = ["grid", "heart"]


class Game:

    def __init__(self):
        self.difficulty = "normal"
        self.clock      = pygame.time.Clock()
        self.playing    = False
        self.win        = False
        self.map_mode   = "grid"          # random pick map new()
        self.width      = 480
        self.height     = 480
        self.screen     = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(TITLE)

    # New game

    def new(self):
        # 1. random map
        self.map_mode = random.choice(MAP_MODES)

        # 2. parameter difficulty
        settings          = DIFFICULTIES[self.difficulty]
        self.rows         = settings["rows"]
        self.cols         = settings["cols"]
        self.amount_mines = random.randint(settings["min_mines"], settings["max_mines"])
        self.max_time     = settings.get("time_limit", 120)

        # 3.Windows size
        if self.map_mode == "heart":
            self.width  = TILESIZE * HEART_COLS
            self.height = TILESIZE * HEART_ROWS
        else:
            self.width  = TILESIZE * self.cols
            self.height = TILESIZE * self.rows
        self.screen = pygame.display.set_mode((self.width, self.height))

        # 4. create board
        if self.map_mode == "heart":
            self.board = Board_Heart(self.amount_mines)
        else:
            self.board = Board(self.rows, self.cols, self.amount_mines)

        self.start_time = pygame.time.get_ticks()
        self.playing    = True
        self.win        = False

    # main loop

    def run(self):
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()

            elapsed   = (pygame.time.get_ticks() - self.start_time) // 1000
            remaining = self.max_time - elapsed
            if remaining <= 0:
                self.playing = False

            if self.board.check_win():
                self.win     = True
                self.playing = False
                for row in self.board.board_list:
                    for tile in row:
                        if not tile.revealed:
                            tile.marker = "flag"
        else:
            self.end_screen()

    # rendered

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen)

        font      = pygame.font.SysFont("Arial", 20)
        elapsed   = (pygame.time.get_ticks() - self.start_time) // 1000
        remaining = max(0, self.max_time - elapsed)

        labels = [
            f"Time : {remaining}s",
            f"Mode : {self.difficulty}",
            f"Map  : {self.map_mode}",
            f"[1] facile  [2] normal  [3] difficile",
        ]
        for i, txt in enumerate(labels):
            surf = font.render(txt, True, WHITE)
            self.screen.blit(surf, (8, 8 + i * 24))

        pygame.display.flip()

    # event

    def events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                col    = mx // TILESIZE
                row    = my // TILESIZE

                if row >= self.board.rows or col >= self.board.cols:
                    continue

                tile = self.board.board_list[row][col]

                if tile.type == "/":   # case outside the core → ignored
                    continue

                if not self.board.mines_placed:
                    self.board.place_mines(row, col)

                # left clic
                if event.button == 1 and tile.marker == "none" and not tile.revealed:
                    if not self.board.dig(row, col):
                        # loose : reveals everything
                        for r in self.board.board_list:
                            for t in r:
                                if t.marker == "flag" and t.type != "X":
                                    t.marker   = "none"
                                    t.revealed = True
                                    t.image    = tile_not_mine
                                elif t.type == "X":
                                    t.revealed = True
                        self.playing = False

                # rigth clic
                elif event.button == 3 and not tile.revealed:
                    tile.toggle_marker()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.difficulty = "facile";  self.new()
                elif event.key == pygame.K_2:
                    self.difficulty = "normal";  self.new()
                elif event.key == pygame.K_3:
                    self.difficulty = "pay";     self.new()

    # end screen

    def end_screen(self):
        font  = pygame.font.SysFont("Arial", 48)
        msg   = "VICTOIRE !" if self.win else "GAME OVER"
        color = (80, 220, 80) if self.win else RED
        text  = font.render(msg, True, color)
        rect  = text.get_rect(center=(self.width // 2, self.height // 2))

        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))

        waiting = True
        while waiting:
            self.clock.tick(FPS)
            self.screen.fill(BGCOLOUR)
            self.board.draw(self.screen)
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(text, rect)
            pygame.display.flip()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); quit(0)
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False


if __name__ == "__main__":
    game = Game()
    while True:
        game.new()
        game.run()