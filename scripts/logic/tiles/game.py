import pygame
pygame.init()
import random
from settings import DIFFICULTIES, TILESIZE, FPS, BGCOLOUR, WHITE, RED, TITLE, tile_not_mine
from board import Board
from Tile_class import Tile

class Game:
    def __init__(self):
        self.difficulty = "normal"  # default
        self.clock = pygame.time.Clock()
        self.playing = False
        self.win = False

        self.set_difficulty(self.difficulty)

    def set_difficulty(self, difficulty):
        """Set board size, mines, and max_time based on difficulty"""
        self.difficulty = difficulty
        settings = DIFFICULTIES[difficulty]
        self.rows = settings["rows"]
        self.cols = settings["cols"]
        self.amount_mines = random.randint(settings["min_mines"], settings["max_mines"])
        self.max_time = settings.get("time_limit", 120)  # seconds
        self.width = TILESIZE * self.cols
        self.height = TILESIZE * self.rows
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(TITLE)

    def new(self):
        self.set_difficulty(self.difficulty)
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

            # Countdown timer
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            remaining_time = self.max_time - elapsed_time
            if remaining_time <= 0:
                self.playing = False  # time over → game over

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

        font = pygame.font.SysFont("Arial", 24)
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        remaining_time = max(0, self.max_time - elapsed_time)
        timer_text = font.render(f"Time: {remaining_time}s", True, WHITE)
        self.screen.blit(timer_text, (10, 10))

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

            # Keyboard difficulty selection
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.set_difficulty("easy")
                    self.new()
                elif event.key == pygame.K_2:
                    self.set_difficulty("normal")
                    self.new()
                elif event.key == pygame.K_3:
                    self.set_difficulty("pay")  # hard mode renamed "pay"
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


# Run the game
if __name__ == "__main__":
    game = Game()
    while True:
        game.new()
        game.run()