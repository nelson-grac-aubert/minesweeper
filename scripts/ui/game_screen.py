import sys
import os
import random
import pygame
import webbrowser

_TILES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'logic', 'tiles'))
if _TILES_DIR not in sys.path:
    sys.path.insert(0, _TILES_DIR)

from scripts.logic.tiles.board        import Board
from scripts.logic.tiles.board_Heart  import Board_Heart, HEART_ROWS, HEART_COLS
from scripts.logic.tiles.settings     import TILESIZE, tile_not_mine, DIFFICULTIES
import scripts.logic.tiles.Tile_class as _tile_module
from scripts.ui.button import Button

from scripts.logic.utils.assets_imports import load_image
from scripts.ui.ui_settings import *
from scripts.ui.pub import AdBanner

_HEADER_H = 70
_PAD      = 20


class GameScreen:

    def __init__(self, screen: pygame.Surface,
                 grid_size: int, num_bombs: int, difficulty: str,
                 unlocked_skins: list, ads_removed: bool = False):  # ← NEW : ads_removed param

        self.map_mode = random.choice(["grid", "grid", "grid", "heart"])

        self.screen         = screen
        self.grid_size      = grid_size
        self.num_bombs      = num_bombs
        self.difficulty     = difficulty
        self.unlocked_skins = unlocked_skins
        self.ads_removed    = ads_removed  # ← NEW : store the flag

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

        _DIFF_MAP       = {"easy": "facile", "medium": "normal", "hard": "pay"}
        settings_key    = _DIFF_MAP.get(difficulty, "normal")
        self.time_limit = DIFFICULTIES[settings_key]["time_limit"]

        self.elapsed_before_shop = 0
        self.start_ticks = pygame.time.get_ticks()
        self.playing     = True
        self.game_over   = False
        self.won         = False

        self._font     = pygame.font.SysFont("Arial", 22, bold=True)

        # Victory / Game Over assets
        self._victory_img   = load_image("assets/images/victory.png")
        self._game_over_img = load_image("assets/images/game_over.png")

        shop_w, shop_h = 160, 50
        self.shop_rect = pygame.Rect(
            WINDOW_W - shop_w - 75,
            WINDOW_H - shop_h - 50,
            shop_w, shop_h,
        )

        back_w, back_h = 160, 50
        self.back_rect = pygame.Rect(
            (WINDOW_W - back_w) // 2,
            WINDOW_H - back_h - 5,
            back_w, back_h,
        )

        # Load banner ads 
        self.buddy_ad = load_image("assets/images/budget_ad.png")
        self.jam_ad = load_image("assets/images/jam_ad.png")
        ad_w, ad_h = self.buddy_ad.get_size() 

        # Ads position
        self.ad_left_rect  = self.buddy_ad.get_rect(midleft=(40, WINDOW_H // 2 + 100))
        self.ad_right_rect = self.jam_ad.get_rect(midright=(WINDOW_W - 40, WINDOW_H // 2 - 30))

        pub_h = 90
        pub_w = 420
        pub_x = self._grid_rect.centerx - pub_w // 2
        pub_y = self._grid_rect.top - pub_h - 10

        self.pub_banner = AdBanner(screen, pub_x, pub_y, pub_w, pub_h)

        self.back_button = Button("assets/images/return_button.png",
                                  self.back_rect.center, 1.5)

        self.all_shop_buttons = []
        self.positions = self.generate_shop_button_positions()

        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], shop_w, shop_h)
            self.all_shop_buttons.append(Button("assets/images/store.png", rect.center, 2))

        # Replay button
        replay_center = (WINDOW_W // 2, self.back_rect.top - 20)
        self.retry_button = Button("assets/images/replay.png",
                                   replay_center, 1.5)

        self._flag_images: dict[str, pygame.Surface] = {}
        for skin, path in SKIN_ASSETS.items():
            raw = load_image(path)
            self._flag_images[skin] = pygame.transform.scale(raw, (TILESIZE, TILESIZE))

        self._current_skin = None
        self._apply_skin(self.unlocked_skins[0])

        self._skin_btn_size   = 36
        self._skin_btn_margin = 8
        self._skin_btns: list[tuple[str, pygame.Rect]] = []

    def generate_shop_button_positions(self):
        positions = []

        shop_w = 160 
        spacing_from_edge = 68

        # Right buttons
        right_x = WINDOW_W - shop_w - spacing_from_edge
        right_y = 5 * WINDOW_H // 6
        positions.append((right_x, right_y))

        # Left buttons
        left_x = spacing_from_edge
        left_y = WINDOW_H // 5
        positions.append((left_x, left_y))

        return positions

    def resume(self):
        """Restore the timer after returning from the shop."""
        self.start_ticks = pygame.time.get_ticks() - self.elapsed_before_shop * 1000

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

            for index, button in enumerate(self.all_shop_buttons):
                if button.rect.collidepoint(event.pos):
                    self.elapsed_before_shop = (pygame.time.get_ticks() - self.start_ticks) // 1000
                    return "shop"
            
            if self.retry_button.is_clicked(event):
                return ("new_game", self.grid_size, self.num_bombs)

            if self.back_rect.collidepoint(event.pos):
                return "home"

            for skin, rect in self._skin_btns:
                if rect.collidepoint(event.pos):
                    self._apply_skin(skin)
                    return None
            
            # Clicking on ads open browers to an ad 
            if not self.ads_removed and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.ad_left_rect.collidepoint(event.pos):
                    webbrowser.open("https://github.com/nelson-grac-aubert/budget_buddy/releases/")
                    return None
                elif self.ad_right_rect.collidepoint(event.pos):
                    webbrowser.open("https://itch.io/jam/brackeys-15/rate/4310895")
                    return None

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

    def update(self, dt_ms: int) -> None:
        """Call every frame with the delta-time in milliseconds."""
        if not self.ads_removed:          # Only update banner if ads are active 
            self.pub_banner.update(dt_ms)

    def draw(self) -> None:
        self.screen.fill(BG_COLOR)

        grid_surf = self.screen.subsurface(self._grid_rect)
        self.board.draw(grid_surf)

        if not self.ads_removed:          # Only draw banner if ads are active 
            self.pub_banner.draw()

        pygame.draw.rect(self.screen, OVERLAY_COLOR,
                         pygame.Rect(0, 0, WINDOW_W, _HEADER_H))
        pygame.draw.line(self.screen, ACCENT_COLOR,
                         (0, _HEADER_H), (WINDOW_W, _HEADER_H), 2)

        # Timer or banner in header
        header_center = (WINDOW_W // 2, _HEADER_H // 2)

        if self.game_over or self.won:
            banner = self._victory_img if self.won else self._game_over_img
            banner_rect = banner.get_rect(center=header_center)
            self.screen.blit(banner, banner_rect)
        else:
            elapsed   = (pygame.time.get_ticks() - self.start_ticks) // 1000
            remaining = max(0, self.time_limit - elapsed)

            if self.playing and remaining == 0:
                self.game_over = True
                self.playing   = False

            # Timer becomes red when time left is short
            timer_color = TIME_COLOR if remaining <= 10 else TEXT_COLOR
            timer_surf  = self._font.render(f"Time left : {remaining}s", True, timer_color)
            self.screen.blit(timer_surf,
                             timer_surf.get_rect(center=header_center))

        # Mode + Diff
        map_label = "♥ Cœur" if self.map_mode == "heart" else "Grille"
        diff_surf = self._font.render(
            f"Mode : {self.difficulty.upper()}  {map_label}", True, ACCENT_COLOR)
        self.screen.blit(diff_surf,
                         diff_surf.get_rect(midright=(WINDOW_W - _PAD, _HEADER_H // 2)))

        # Skins
        self._rebuild_skin_buttons()
        for skin, rect in self._skin_btns:
            is_active  = (skin == self._current_skin)
            bg_col     = ACCENT_COLOR if is_active else OVERLAY_COLOR
            pygame.draw.rect(self.screen, bg_col, rect, border_radius=6)
            flag_img   = self._flag_images[skin]
            self.screen.blit(flag_img, flag_img.get_rect(center=rect.center))
            border_col = TEXT_COLOR if is_active else (88, 91, 112)
            pygame.draw.rect(self.screen, border_col, rect, width=2, border_radius=6)

        # Navigation buttons
        self.retry_button.draw(self.screen)
        self.back_button.draw(self.screen)

        # 2 shop buttons 
        for button in self.all_shop_buttons:
            button.draw(self.screen)

        # Ads
        if not self.ads_removed:
            self.screen.blit(self.buddy_ad, self.ad_left_rect)
            self.screen.blit(self.jam_ad, self.ad_right_rect)

