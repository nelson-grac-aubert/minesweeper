import sys
import os
import random
import pygame

_TILES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'logic', 'tiles'))
if _TILES_DIR not in sys.path:
    sys.path.insert(0, _TILES_DIR)

from scripts.logic.tiles.board import Board
from scripts.logic.tiles.board_Heart import Board_Heart, HEART_ROWS, HEART_COLS
from scripts.logic.tiles.settings import TILESIZE, tile_not_mine, DIFFICULTIES

from scripts.ui.ui_settings import (
    BG_COLOR, OVERLAY_COLOR, TEXT_COLOR, ACCENT_COLOR, BACK_COLOR,
    WINDOW_W, WINDOW_H,
)

_HEADER_H = 70
_PAD      = 20


class GameScreen:

    def __init__(self, screen: pygame.Surface,
                 grid_size: int, num_bombs: int, difficulty: str):
        self.screen     = screen
        self.grid_size  = grid_size
        self.num_bombs  = num_bombs
        self.difficulty = difficulty

        self.map_mode = random.choice(["grid", "heart"])

        if self.map_mode == "heart":
            self.board  = Board_Heart(num_bombs)
            board_cols  = HEART_COLS
            board_rows  = HEART_ROWS
        else:
            self.board  = Board(grid_size, grid_size, num_bombs)
            board_cols  = grid_size
            board_rows  = grid_size

        gpx    = board_cols * TILESIZE
        gpy    = board_rows * TILESIZE
        play_h = WINDOW_H - _HEADER_H - _PAD * 2
        self.ox = (WINDOW_W - gpx) // 2
        self.oy = _HEADER_H + _PAD + max(0, (play_h - gpy) // 2)
        self._grid_rect = pygame.Rect(self.ox, self.oy, gpx, gpy)

        _DIFF_MAP    = {"easy": "facile", "medium": "normal", "hard": "pay"}
        settings_key = _DIFF_MAP.get(difficulty, "normal")
        self.time_limit = DIFFICULTIES[settings_key]["time_limit"]

        self.elapsed_before_shop = 0
        self.start_ticks = pygame.time.get_ticks()
        self.playing     = True
        self.game_over   = False
        self.won         = False

        self._font      = pygame.font.SysFont("Arial", 22, bold=True)
        self._font_big  = pygame.font.SysFont("Arial", 52, bold=True)
        self._font_sub  = pygame.font.SysFont("Arial", 20)
        self._font_back = pygame.font.SysFont("monospace", 20, bold=True)

        # ── bouton Shop (coin bas-droit, toujours visible) ────────────────
        shop_w, shop_h = 160, 50
        self.shop_rect = pygame.Rect(
            WINDOW_W - shop_w - 30,
            WINDOW_H - shop_h - 30,
            shop_w, shop_h,
        )

        # ── boutons fin de partie 
        btn_w, btn_h = 180, 50
        center_y     = WINDOW_H // 2 - 80          # sous le message GAME OVER
        self.retry_rect = pygame.Rect(
            WINDOW_W // 2 - btn_w - 20, center_y, btn_w, btn_h)
        self.home_rect  = pygame.Rect(
            WINDOW_W // 2 + 20,          center_y, btn_w, btn_h)

    # ── resume après shop 

    def resume(self):
        self.start_ticks = pygame.time.get_ticks() - self.elapsed_before_shop * 1000

    # ── événements 

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # Bouton shop (toujours cliquable)
            if self.shop_rect.collidepoint(event.pos):
                self.elapsed_before_shop = (
                    pygame.time.get_ticks() - self.start_ticks) // 1000
                return "shop"

            # Boutons fin de partie (seulement quand game over / victoire)
            if self.game_over or self.won:
                if self.retry_rect.collidepoint(event.pos):
                    return ("new_game", self.grid_size, self.num_bombs)
                if self.home_rect.collidepoint(event.pos):
                    return "home"

        if not self.playing:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if not self._grid_rect.collidepoint(mx, my):
                return None

            col = (mx - self.ox) // TILESIZE
            row = (my - self.oy) // TILESIZE

            if not (0 <= row < self.board.rows and 0 <= col < self.board.cols):
                return None

            tile = self.board.board_list[row][col]

            if tile.type == "/":
                return None

            if not self.board.mines_placed:
                self.board.place_mines(row, col)

            if event.button == 1 and tile.marker == "none" and not tile.revealed:
                if not self.board.dig(row, col):
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
                    for board_row in self.board.board_list:
                        for t in board_row:
                            if not t.revealed:
                                t.marker = "flag"
                    self.won     = True
                    self.playing = False

            elif event.button == 3 and not tile.revealed:
                tile.toggle_marker()

        return None

    # ── rendu 

    def draw(self) -> None:
        self.screen.fill(BG_COLOR)

        grid_surf = self.screen.subsurface(self._grid_rect)
        self.board.draw(grid_surf)

        # Barre du haut
        pygame.draw.rect(self.screen, OVERLAY_COLOR,
                         pygame.Rect(0, 0, WINDOW_W, _HEADER_H))
        pygame.draw.line(self.screen, ACCENT_COLOR,
                         (0, _HEADER_H), (WINDOW_W, _HEADER_H), 2)

        elapsed   = (pygame.time.get_ticks() - self.start_ticks) // 1000
        remaining = max(0, self.time_limit - elapsed)

        if self.playing and remaining == 0:
            self.game_over = True
            self.playing   = False

        timer_color = (243, 139, 168) if remaining <= 10 else TEXT_COLOR
        timer_surf  = self._font.render(f"Temps restant : {remaining}s", True, timer_color)
        self.screen.blit(timer_surf,
                         timer_surf.get_rect(center=(WINDOW_W // 2, _HEADER_H // 2)))

        map_label = "♥ Cœur" if self.map_mode == "heart" else "⊞ Grille"
        diff_surf = self._font.render(
            f"Mode : {self.difficulty.upper()}  {map_label}", True, ACCENT_COLOR)
        self.screen.blit(diff_surf,
                         diff_surf.get_rect(midright=(WINDOW_W - 20, _HEADER_H // 2)))

        # Bouton Shop
        self._draw_btn(self.shop_rect, "Shop", accent=True)

        # ── overlay fin de partie 
        if self.game_over or self.won:
            overlay = pygame.Surface((WINDOW_W, WINDOW_H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            msg     = "VICTOIRE !" if self.won else "GAME OVER"
            msg_col = (166, 227, 161) if self.won else (243, 139, 168)
            big     = self._font_big.render(msg, True, msg_col)
            self.screen.blit(big, big.get_rect(
                center=(WINDOW_W // 2, WINDOW_H // 2 - 180)))

            # Bouton Rejouer (gauche)
            self._draw_btn(self.retry_rect, "Rejouer")

            # Bouton Menu (droite)
            self._draw_btn(self.home_rect, "⌂ Menu")

    # ── helper bouton 

    def _draw_btn(self, rect: pygame.Rect, label: str, accent: bool = False):
        hover = rect.collidepoint(pygame.mouse.get_pos())
        if accent:
            bg = ACCENT_COLOR if not hover else TEXT_COLOR
            fg = BG_COLOR
        else:
            bg = ACCENT_COLOR if hover else BACK_COLOR
            fg = BG_COLOR if hover else TEXT_COLOR
        pygame.draw.rect(self.screen, bg, rect, border_radius=10)
        surf = self._font_back.render(label, True, fg)
        self.screen.blit(surf, surf.get_rect(center=rect.center))