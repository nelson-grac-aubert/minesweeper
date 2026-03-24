import pygame
from settings import *
from board import *
from Tile_class import *


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def new(self):
        self.board = Board()
        self.board.display_board()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
        else:
            self.end_screen()

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen)
        pygame.display.flip()

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "X" and not tile.revealed:
                    return False
        return True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx //= TILESIZE
                my //= TILESIZE

                tile = self.board.board_list[mx][my]

                # left clic
                if event.button == 1:
                    if tile.marker == "none" and not tile.revealed:
                        if not self.board.dig(mx, my):
                            # Explosion
                            for row in self.board.board_list:
                                for t in row:
                                    if t.marker == "flag" and t.type != "X":
                                        t.marker = "none"
                                        t.revealed = True
                                        t.image = tile_not_mine
                                    elif t.type == "X":
                                        t.revealed = True
                            self.playing = False

                # rigth clic
                elif event.button == 3:
                    if not tile.revealed:
                        tile.toggle_marker()

                # CHECK WIN
                if self.check_win():
                    self.win = True
                    self.playing = False
                    for row in self.board.board_list:
                        for t in row:
                            if not t.revealed:
                                t.marker = "flag"

    def end_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    return


game = Game()
while True:
    game.new()
    game.run()