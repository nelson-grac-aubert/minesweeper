import pygame
pygame.init()
import random
from settings import DIFFICULTIES, TILESIZE, FPS, BGCOLOUR, WHITE, RED, TITLE
from board import Board
from settings import tile_not_mine

class Game:
    """Main game logic for Minesweeper."""
    def __init__(self):
        self.difficulty = "normal"
        self.clock = pygame.time.Clock()
        self.playing = False
        self.win = False
        self.set_difficulty(self.difficulty)

    def set_difficulty(self, difficulty):
        """Update game parameters based on difficulty."""
        self.difficulty = difficulty
        settings = DIFFICULTIES[difficulty]
        self.rows = settings["rows"]
        self.cols = settings["cols"]
        self.amount_mines = random.randint(settings["min_mines"], settings["max_mines"])
        self.max_time = settings.get("time_limit", 120)
        self.width = TILESIZE * self.cols
        self.height = TILESIZE * self.rows
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(TITLE)

    def new(self):
        """Start a new game."""
        self.set_difficulty(self.difficulty)
        self.board = Board(self.rows, self.cols, self.amount_mines)
        self.start_time = pygame.time.get_ticks()
        self.playing = True
        self.win = False

    def run(self):
        """Main game loop."""
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()

            elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
            remaining = self.max_time - elapsed
            if remaining <= 0:
                self.playing = False

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
        elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
        remaining = max(0, self.max_time - elapsed)
        timer_text = font.render(f"Time: {remaining}s", True, WHITE)
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
                col = mx // TILESIZE
                row = my // TILESIZE
                if row >= self.rows or col >= self.cols:
                    continue
                tile = self.board.board_list[row][col]

                # Place mines safely on first click
                if not self.board.mines_placed:
                    self.board.place_mines(row, col)

                # LEFT click
                if event.button == 1 and tile.marker == "none":
                    if not self.board.dig(row, col):
                        for r in self.board.board_list:
                            for t in r:
                                if t.marker == "flag" and t.type != "X":
                                    t.marker = "none"
                                    t.revealed = True
                                    t.image = tile_not_mine
                                elif t.type == "X":
                                    t.revealed = True
                        self.playing = False

                # RIGHT click
                elif event.button == 3 and not tile.revealed:
                    tile.toggle_marker()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.set_difficulty("easy")
                    self.new()
                elif event.key == pygame.K_2:
                    self.set_difficulty("normal")
                    self.new()
                elif event.key == pygame.K_3:
                    self.set_difficulty("pay")
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