import sys
import os
import pygame

# Add the colleague's tiles directory to sys.path so their bare imports work
_TILES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'logic', 'tiles'))
if _TILES_DIR not in sys.path:
    sys.path.insert(0, _TILES_DIR)

from scripts.logic.tiles.board    import Board
from scripts.logic.tiles.settings import TILESIZE, tile_not_mine, DIFFICULTIES
import scripts.logic.tiles.Tile_class as _tile_module

from scripts.logic.utils.assets_imports import load_image
from scripts.ui.ui_settings import *

_HEADER_H = 70
_PAD      = 20

class GameScreen:

    def __init__(self, screen: pygame.Surface,
                 grid_size: int, num_bombs: int, difficulty: str,
                 unlocked_skins: list):

        self.screen         = screen
        self.grid_size      = grid_size
        self.num_bombs      = num_bombs
        self.difficulty     = difficulty
        self.unlocked_skins = unlocked_skins

        self.board = Board(grid_size, grid_size, num_bombs)

        # Center the grid below the header
        gpx    = grid_size * TILESIZE
        gpy    = grid_size * TILESIZE
        play_h = WINDOW_H - _HEADER_H - _PAD * 2
        self.ox = (WINDOW_W - gpx) // 2
        self.oy = _HEADER_H + _PAD + max(0, (play_h - gpy) // 2)
        self._grid_rect = pygame.Rect(self.ox, self.oy, gpx, gpy)

        # Map UI difficulty name to the colleague's settings key
        _DIFF_MAP       = {"easy": "facile", "medium": "normal", "hard": "pay"}
        settings_key    = _DIFF_MAP.get(difficulty, "normal")
        self.time_limit = DIFFICULTIES[settings_key]["time_limit"]

        self.start_ticks = pygame.time.get_ticks()
        self.playing     = True
        self.game_over   = False
        self.won         = False

        self._font      = pygame.font.SysFont("Arial", 22, bold=True)
        self._font_big  = pygame.font.SysFont("Arial", 52, bold=True)
        self._font_sub  = pygame.font.SysFont("Arial", 20)
        self._font_back = pygame.font.SysFont("monospace", 20, bold=True)

        back_w, back_h = 160, 50
        self.back_rect = pygame.Rect(
            (WINDOW_W - back_w) // 2,
            WINDOW_H - back_h - 40,
            back_w, back_h,
        )

        # Pre-load all flag sprites scaled to TILESIZE
        self._flag_images: dict[str, pygame.Surface] = {}
        for skin, path in SKIN_ASSETS.items():
            raw = load_image(path)
            self._flag_images[skin] = pygame.transform.scale(raw, (TILESIZE, TILESIZE))

        self._current_skin = None
        self._apply_skin(self.unlocked_skins[0])

        self._skin_btn_size   = 36
        self._skin_btn_margin = 8
        self._skin_btns: list[tuple[str, pygame.Rect]] = []

    def _apply_skin(self, skin: str) -> None:
        """Patch Tile_class.tile_flag so Tile.draw() uses the selected sprite."""
        self._current_skin = skin
        _tile_module.tile_flag = self._flag_images[skin]

    def _rebuild_skin_buttons(self) -> None:
        """Recompute header button rects based on currently unlocked skins."""
        self._skin_btns.clear()
        x = _PAD
        y = (_HEADER_H - self._skin_btn_size) // 2
        for skin in self.unlocked_skins:
            rect = pygame.Rect(x, y, self._skin_btn_size, self._skin_btn_size)
            self._skin_btns.append((skin, rect))
            x += self._skin_btn_size + self._skin_btn_margin

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.back_rect.collidepoint(event.pos):
                return "home"

            for skin, rect in self._skin_btns:
                if rect.collidepoint(event.pos):
                    self._apply_skin(skin)
                    return None

        if not self.playing:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if not self._grid_rect.collidepoint(mx, my):
                return None

            col  = (mx - self.ox) // TILESIZE
            row  = (my - self.oy) // TILESIZE
            tile = self.board.board_list[row][col]

            # Place mines on first click, keeping the clicked cell and its neighbors safe
            if not self.board.mines_placed:
                self.board.place_mines(row, col)

            if event.button == 1 and tile.marker == "none" and not tile.revealed:
                if not self.board.dig(row, col):
                    # Mine hit: reveal the whole board
                    for board_row in self.board.board_list:
                        for t in board_row:
                            if t.marker == "flag" and t.type != "X":
                                t.marker   = "none"
                                t.revealed = True
                                t.image    = tile_not_mine
                            elif t.type == "X":
                                t.revealed = True
                    self.game_over = True
                    self.playing   = False

                elif self.board.check_win():
                    # Flag all remaining mines
                    for board_row in self.board.board_list:
                        for t in board_row:
                            if not t.revealed:
                                t.marker = "flag"
                    self.won     = True
                    self.playing = False

            elif event.button == 3 and not tile.revealed:
                tile.toggle_marker()

        return None

    def draw(self) -> None:
        self.screen.fill(BG_COLOR)

        # Draw the board onto a subsurface for (0,0) coordinates always
        grid_surf = self.screen.subsurface(self._grid_rect)
        self.board.draw(grid_surf)

        # Header background
        pygame.draw.rect(self.screen, OVERLAY_COLOR,
                         pygame.Rect(0, 0, WINDOW_W, _HEADER_H))
        pygame.draw.line(self.screen, ACCENT_COLOR,
                         (0, _HEADER_H), (WINDOW_W, _HEADER_H), 2)

        # Countdown timer (turns red under 10 seconds)
        elapsed   = (pygame.time.get_ticks() - self.start_ticks) // 1000
        remaining = max(0, self.time_limit - elapsed)
        if self.playing and remaining == 0:
            self.game_over = True
            self.playing   = False
        timer_color = (243, 139, 168) if remaining <= 10 else TEXT_COLOR
        timer_surf  = self._font.render(f"Time left : {remaining}s", True, timer_color)
        self.screen.blit(timer_surf,
                         timer_surf.get_rect(center=(WINDOW_W // 2, _HEADER_H // 2)))

        # Difficulty label (right side of header)
        diff_surf = self._font.render(
            f"Mode : {self.difficulty.upper()}", True, ACCENT_COLOR)
        self.screen.blit(diff_surf,
                         diff_surf.get_rect(midright=(WINDOW_W - _PAD, _HEADER_H // 2)))

        # Flag skin selector (left side of header)
        self._rebuild_skin_buttons()
        for skin, rect in self._skin_btns:
            is_active  = (skin == self._current_skin)
            bg_col     = ACCENT_COLOR if is_active else OVERLAY_COLOR
            pygame.draw.rect(self.screen, bg_col, rect, border_radius=6)
            flag_img   = self._flag_images[skin]
            self.screen.blit(flag_img, flag_img.get_rect(center=rect.center))
            border_col = TEXT_COLOR if is_active else (88, 91, 112)
            pygame.draw.rect(self.screen, border_col, rect, width=2, border_radius=6)

        # Back button
        hover = self.back_rect.collidepoint(pygame.mouse.get_pos())
        color = ACCENT_COLOR if hover else BACK_COLOR
        pygame.draw.rect(self.screen, color, self.back_rect, border_radius=10)
        label = self._font_back.render(
            "← Retour", True, BG_COLOR if hover else TEXT_COLOR)
        self.screen.blit(label, label.get_rect(center=self.back_rect.center))

        # End-of-game overlay
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