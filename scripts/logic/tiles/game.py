# game.py — point d'entrée
import os
import sys
import random
import importlib.util
import pygame

import settings
from settings import TILESIZE, FPS, TITLE, BGCOLOUR, DIFFICULTIES, init_images

MAPS = ["classic", "heart"]


class Game:
    def __init__(self):
        pygame.init()

        # Résolution du chemin vers assets/images/
        # game.py est dans  MINESWEEPER/scripts/logic/tiles/
        # assets/images/ est dans  MINESWEEPER/assets/images/
        tiles_dir    = os.path.dirname(os.path.abspath(__file__))
        scripts_dir  = os.path.dirname(os.path.dirname(tiles_dir))
        root_dir     = os.path.dirname(scripts_dir)
        self.assets_dir = os.path.join(root_dir, "assets", "images")

        # set_mode AVANT init_images (convert_alpha exige une fenêtre ouverte)
        self.screen = pygame.display.set_mode((480, 480))
        self.clock  = pygame.time.Clock()

        init_images(self.assets_dir)

    def new(self):
        self.run()

    def run(self):
        while True:
            self._play()

    # ---------------------------------------------------------------- privé

    def _load_board_module(self, map_name):
        """Importe dynamiquement maps/<map_name>/board.py."""
        tiles_dir  = os.path.dirname(os.path.abspath(__file__))
        path       = os.path.join(tiles_dir, "maps", map_name, "board.py")
        spec       = importlib.util.spec_from_file_location(f"{map_name}.board", path)
        module     = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _play(self):
        # Choix aléatoire de la carte et de la difficulté
        map_name   = random.choice(MAPS)
        difficulty = random.choice(list(DIFFICULTIES.keys()))
        diff       = DIFFICULTIES[difficulty]

        rows         = diff["rows"]
        cols         = diff["cols"]
        amount_mines = random.randint(diff["min_mines"], diff["max_mines"])

        module = self._load_board_module(map_name)
        board  = module.Board(rows, cols, amount_mines)

        width  = board.cols * TILESIZE
        height = board.rows * TILESIZE

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"{TITLE}  —  {map_name}  [{difficulty}]")

        playing = True
        won     = False

        while playing:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // TILESIZE
                    row = event.pos[1] // TILESIZE

                    # Vérifie que la case est dans les limites et jouable
                    if not (0 <= row < board.rows and 0 <= col < board.cols):
                        continue
                    if hasattr(board, "is_playable") and not board.is_playable(row, col):
                        continue

                    tile = board.board_list[row][col]

                    # Clic gauche : révèle
                    if event.button == 1 and tile.marker == "none" and not tile.revealed:
                        if not board.mines_placed:
                            board.place_mines(row, col)
                        if not board.dig(row, col):
                            board.reveal_all_mines()
                            playing = False
                        elif board.check_win():
                            won = True
                            playing = False

                    # Clic droit : cycle none → flag → question → none
                    elif event.button == 3 and not tile.revealed:
                        tile.toggle_marker()

            self.screen.fill(BGCOLOUR)
            board.draw(self.screen)
            pygame.display.flip()

        self._end_screen(board, won, width, height)

    def _end_screen(self, board, won, width, height):
        font = pygame.font.SysFont(None, 48)
        msg  = "Gagné !  Cliquez pour rejouer" if won else "Perdu !  Cliquez pour rejouer"
        text = font.render(msg, True, (255, 255, 255))
        rect = text.get_rect(center=(width // 2, height // 2))

        waiting = True
        while waiting:
            self.clock.tick(FPS)
            self.screen.fill(BGCOLOUR)
            board.draw(self.screen)
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(text, rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False


if __name__ == "__main__":
    Game().run()