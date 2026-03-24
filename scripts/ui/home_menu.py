import pygame
import random

from scripts.ui.button            import Button
from scripts.ui.difficulty_button import DifficultyButton

BG_COLOR      = (30,  30,  46)
OVERLAY_COLOR = (49,  50,  68)

DIFFICULTY_PARAMS = {
    "easy":   {"grid": 8,  "bombs_min": 5,  "bombs_max": 7},
    "medium": {"grid": 10, "bombs_min": 7,  "bombs_max": 9},
    "hard":   {"grid": 12, "bombs_min": 30, "bombs_max": 40},
}


class HomeMenu:

    W, H = 1000, 680

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        cx = self.W // 2

        # Title
        from scripts.logic.utils.assets_imports import load_image
        raw_title = load_image("assets/images/title.png")
        tw, th    = raw_title.get_size()
        self.title_img  = pygame.transform.scale(raw_title, (tw * 4, th * 4))
        self.title_rect = self.title_img.get_rect(center=(cx, 100))

        # Buttons
        self.btn_new_game   = Button("assets/images/new_game.png", center=(cx, 270))
        self.btn_difficulty = DifficultyButton(center=(cx, 360))
        self.btn_options    = Button("assets/images/options.png",  center=(cx, 450))
        self.btn_shop       = Button("assets/images/store.png",    center=(cx, 560))

    def handle_event(self, event: pygame.event.Event):
        if self.btn_difficulty.is_clicked(event):
            return None

        if self.btn_new_game.is_clicked(event):
            diff   = self.btn_difficulty.current
            params = DIFFICULTY_PARAMS[diff]
            bombs  = random.randint(params["bombs_min"], params["bombs_max"])
            return ("new_game", params["grid"], bombs)

        if self.btn_options.is_clicked(event):
            return "options"

        if self.btn_shop.is_clicked(event):
            return "shop"

        return None

    def draw(self) -> None:
        self.screen.fill(BG_COLOR)
        self._draw_card()
        self.screen.blit(self.title_img, self.title_rect)
        self.btn_new_game.draw(self.screen)
        self.btn_difficulty.draw(self.screen)
        self.btn_options.draw(self.screen)
        self.btn_shop.draw(self.screen)

    def _draw_card(self) -> None:
        margin = 250
        card = pygame.Rect(margin, 220, self.W - 2 * margin, 430)
        pygame.draw.rect(self.screen, OVERLAY_COLOR, card, border_radius=16)