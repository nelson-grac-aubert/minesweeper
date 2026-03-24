import pygame

from scripts.logic.tiles.board import Board        
from scripts.logic.tiles.settings import TILESIZE, tile_not_mine 

from scripts.ui.ui_settings import (
    BG_COLOR, OVERLAY_COLOR, TEXT_COLOR, ACCENT_COLOR, BACK_COLOR,
    WINDOW_W, WINDOW_H,
)

_HEADER_H = 70   # Top bar size (time, difficulty)
_PAD      = 20   # Margin around board

class GameScreen:

    def __init__(self, screen: pygame.Surface,
                 grid_size: int, num_bombs: int, difficulty: str):
        self.screen     = screen
        self.grid_size  = grid_size
        self.num_bombs  = num_bombs
        self.difficulty = difficulty  # "easy" | "medium" | "pay"

        self.board = Board(grid_size, grid_size, num_bombs)

        # Grid position
        gpx    = grid_size * TILESIZE
        gpy    = grid_size * TILESIZE
        play_h = WINDOW_H - _HEADER_H - _PAD * 2
        self.ox = (WINDOW_W - gpx) // 2
        self.oy = _HEADER_H + _PAD + max(0, (play_h - gpy) // 2)
        self._grid_rect = pygame.Rect(self.ox, self.oy, gpx, gpy)

        # Game State
        self.start_ticks = pygame.time.get_ticks()
        self.playing     = True
        self.game_over   = False
        self.won         = False

        # Fonts
        self._font      = pygame.font.SysFont("Arial", 22, bold=True)
        self._font_big  = pygame.font.SysFont("Arial", 52, bold=True)
        self._font_sub  = pygame.font.SysFont("Arial", 20)
        self._font_back = pygame.font.SysFont("monospace", 20, bold=True)

        # Return Button
        back_w, back_h = 160, 50
        self.back_rect = pygame.Rect(
            (WINDOW_W - back_w) // 2,
            WINDOW_H - back_h - 40,
            back_w, back_h,
        )

    # Events

    def handle_event(self, event: pygame.event.Event):
        # Retun button
        if (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.back_rect.collidepoint(event.pos)):
            return "home"

        if not self.playing:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Check click is on grid
            if not self._grid_rect.collidepoint(mx, my):
                return None

            # Convert to grid coordinates
            col = (mx - self.ox) // TILESIZE
            row = (my - self.oy) // TILESIZE

            tile = self.board.board_list[row][col]

            # First click : places bombs
            if not self.board.mines_placed:
                self.board.place_mines(row, col)

            # Left click : dig
            if event.button == 1 and tile.marker == "none" and not tile.revealed:
                if not self.board.dig(row, col):
                    # Touch mine : reveal board
                    for board_row in self.board.board_list:
                        for t in board_row:
                            if t.marker == "flag" and t.type != "X":
                                # Misplaced flag
                                t.marker   = "none"
                                t.revealed = True
                                t.image    = tile_not_mine
                            elif t.type == "X":
                                t.revealed = True
                    self.game_over = True
                    self.playing   = False

                elif self.board.check_win():
                    # Victory : flag all mines
                    for board_row in self.board.board_list:
                        for t in board_row:
                            if not t.revealed:
                                t.marker = "flag"
                    self.won     = True
                    self.playing = False

            # Right click : drop flag
            elif event.button == 3 and not tile.revealed:
                tile.toggle_marker()

        return None

    # Render

    def draw(self) -> None:
        self.screen.fill(BG_COLOR)

        # Board on a pygame subsurface middle of the screen
        grid_surf = self.screen.subsurface(self._grid_rect)
        self.board.draw(grid_surf)

        # Top pannel
        pygame.draw.rect(self.screen, OVERLAY_COLOR,
                         pygame.Rect(0, 0, WINDOW_W, _HEADER_H))
        pygame.draw.line(self.screen, ACCENT_COLOR,
                         (0, _HEADER_H), (WINDOW_W, _HEADER_H), 2)

        elapsed     = (pygame.time.get_ticks() - self.start_ticks) // 1000
        timer_surf  = self._font.render(f"Temps : {elapsed}s", True, TEXT_COLOR)
        self.screen.blit(timer_surf,
                         timer_surf.get_rect(center=(WINDOW_W // 2, _HEADER_H // 2)))

        diff_surf = self._font.render(
            f"Mode : {self.difficulty.upper()}", True, ACCENT_COLOR)
        self.screen.blit(diff_surf,
                         diff_surf.get_rect(midright=(WINDOW_W - 20, _HEADER_H // 2)))

        # Return button
        hover = self.back_rect.collidepoint(pygame.mouse.get_pos())
        color = ACCENT_COLOR if hover else BACK_COLOR
        pygame.draw.rect(self.screen, color, self.back_rect, border_radius=10)
        label = self._font_back.render(
            "← Retour", True, BG_COLOR if hover else TEXT_COLOR)
        self.screen.blit(label, label.get_rect(center=self.back_rect.center))

        # Game over overlay
        if self.game_over or self.won:
            overlay = pygame.Surface((WINDOW_W, WINDOW_H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            msg     = "VICTOIRE !" if self.won else "GAME OVER"
            msg_col = (166, 227, 161) if self.won else (243, 139, 168)
            big     = self._font_big.render(msg, True, msg_col)
            self.screen.blit(big, big.get_rect(
                center=(WINDOW_W // 2, WINDOW_H // 2 - 220)))

            sub = self._font_sub.render(
                "Clique sur  ← Retour  pour revenir au menu",
                True, TEXT_COLOR)
            self.screen.blit(sub, sub.get_rect(
                center=(WINDOW_W // 2, WINDOW_H // 2 - 180)))