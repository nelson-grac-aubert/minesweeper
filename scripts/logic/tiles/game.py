import pygame
pygame.init()
import random
from settings import *
from board import Board
from Tile_class import Tile

MAX_TIME = 120  # seconds countdown

class Game:
    def __init__(self):
        self.difficulty = "normal"
        self.clock = pygame.time.Clock()
        self.playing = False
        self.win = False

        # dynamic board dimensions
        self.rows = DIFFICULTIES[self.difficulty]["rows"]
        self.cols = DIFFICULTIES[self.difficulty]["cols"]
        self.amount_mines = random.randint(
            DIFFICULTIES[self.difficulty]["min_mines"],
            DIFFICULTIES[self.difficulty]["max_mines"]
        )

        self.width = TILESIZE * self.cols
        self.height = TILESIZE * self.rows
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(TITLE)

    def new(self):
        settings = DIFFICULTIES[self.difficulty]
        self.rows = settings["rows"]
        self.cols = settings["cols"]
        self.amount_mines = random.randint(settings["min_mines"], settings["max_mines"])
        self.width = TILESIZE * self.cols
        self.height = TILESIZE * self.rows
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.board = Board(self.rows, self.cols, self.amount_mines)
        self.board.display_board()
        self.start_time = pygame.time.get_ticks()
        self.playing = True
        self.win = False

    def run(self):
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()

            # Countdown logic
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            remaining_time = MAX_TIME - elapsed_time
            if remaining_time <= 0:
                self.playing = False  # game over by time

            # Check win
            if self.check_win():
                self.win = True
                self.playing = False
                for row in self.board.board_list:
                    for tile in row:
                        if not tile.revealed:
                            tile.marker = "flag"

        else:
            self.end_screen()

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen)

        # Countdown Timer
        font = pygame.font.SysFont("Arial", 24)
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        remaining_time = max(0, MAX_TIME - elapsed_time)
        timer_text = font.render(f"Time: {remaining_time}s", True, WHITE)
        self.screen.blit(timer_text, (10, 10))

        # Difficulty display
        diff_text = font.render(f"Mode: {self.difficulty}", True, WHITE)
        self.screen.blit(diff_text, (10, 40))

        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx //= TILESIZE
                my //= TILESIZE

                if mx >= self.cols or my >= self.rows:
                    continue

                tile = self.board.board_list[mx][my]

                # LEFT CLICK
                if event.button == 1 and tile.marker == "none":
                    if not self.board.dig(mx, my):
                        # Explosion logic
                        for row in self.board.board_list:
                            for t in row:
                                if t.marker == "flag" and t.type != "X":
                                    t.marker = "none"
                                    t.revealed = True
                                    t.image = tile_not_mine
                                elif t.type == "X":
                                    t.revealed = True
                        self.playing = False

                # RIGHT CLICK
                elif event.button == 3 and not tile.revealed:
                    tile.toggle_marker()

            # Keyboard difficulty (1,2,3)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.difficulty = "easy"
                    self.new()
                elif event.key == pygame.K_2:
                    self.difficulty = "normal"
                    self.new()
                elif event.key == pygame.K_3:
                    self.difficulty = "payhard"
                    self.new()

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "X" and not tile.revealed:
                    return False
        return True

    def end_screen(self):
        font = pygame.font.SysFont("Arial", 48)
        text = font.render("GAME OVER", True, RED)
        self.screen.blit(text, (self.width // 2 - 150, self.height // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)


# Run game
if __name__ == "__main__":
    game = Game()
    while True:
        game.new()
        game.run()