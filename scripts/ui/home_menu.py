import pygame
import random
import sys
import os

# always resolve path from root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "logic", "utils"))
from scripts.logic.utils.assets_imports import load_image

# Difficulty constants
DIFFICULTIES = ["easy", "medium", "hard"]

DIFFICULTY_PARAMS = {
    "easy":   {"grid": 8,  "bombs_min": 5,  "bombs_max": 7},
    "medium": {"grid": 10, "bombs_min": 7,  "bombs_max": 9},
    "hard":   {"grid": 12, "bombs_min": 30, "bombs_max": 40},
}


BG_COLOR      = (30,  30,  46)   # dark background
OVERLAY_COLOR = (49,  50,  68)   # light card
ACCENT_COLOR  = (137, 180, 250)  # dark blue
HOVER_TINT    = (255, 255, 255, 30)


class Button:
    """Bouton cliquable à partir d'une image PNG scalée."""

    SCALE = 3 # zoom factor for pixel art assets

    def __init__(self, image_path: str, center: tuple[int, int]):
        raw = load_image(image_path)
        w, h = raw.get_size()
        self.image = pygame.transform.scale(raw, (w * self.SCALE, h * self.SCALE))
        self.rect  = self.image.get_rect(center=center)

        # hover buttons
        self._hover_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self._hover_surf.fill((255, 255, 255, 40))

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self._hover_surf, self.rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class DifficultyButton(Button):
    """Special button : shows easy/medium/pay and changes on click"""

    def __init__(self, center: tuple[int, int]):
        self._index = 0
        self._images: dict[str, pygame.Surface] = {}

        for name in DIFFICULTIES:
            raw = load_image(f"assets/images/{name}.png")
            w, h = raw.get_size()
            self._images[name] = pygame.transform.scale(raw, (w * self.SCALE, h * self.SCALE))

        # starts "easy"
        self.image = self._images["easy"]
        self.rect  = self.image.get_rect(center=center)
        self._hover_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self._hover_surf.fill((255, 255, 255, 40))

    @property
    def current(self) -> str:
        return DIFFICULTIES[self._index]

    def cycle(self) -> None:
        self._index = (self._index + 1) % len(DIFFICULTIES)
        self.image  = self._images[self.current]

    def is_clicked(self, event: pygame.event.Event) -> bool:
        clicked = super().is_clicked(event)
        if clicked:
            self.cycle()
        return clicked


class HomeMenu:

    W, H = 1000, 680

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        cx = self.W // 2  # horizontal center

        # Title
        raw_title = load_image("assets/images/title.png")
        tw, th    = raw_title.get_size()
        self.title_img  = pygame.transform.scale(raw_title, (tw * 4, th * 4))
        self.title_rect = self.title_img.get_rect(center=(cx, 100))

        # Buttons
        self.btn_new_game   = Button("assets/images/new_game.png", center=(cx, 270))
        self.btn_difficulty = DifficultyButton(center=(cx, 360))
        self.btn_options    = Button("assets/images/options.png",  center=(cx, 450))
        self.btn_shop   = Button("assets/images/store.png",    center=(cx, 560))


    def handle_event(self, event: pygame.event.Event):
        """ Handle events, return an action or None """
        if self.btn_difficulty.is_clicked(event):
            return None  # Change difficulty

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
        """ Draw main menu """
        self.screen.fill(BG_COLOR)
        self._draw_card()
        self.screen.blit(self.title_img, self.title_rect)
        self.btn_difficulty.draw(self.screen)
        self.btn_new_game.draw(self.screen)
        self.btn_options.draw(self.screen)
        self.btn_shop.draw(self.screen)

    def _draw_card(self) -> None:
        """ Light card behind buttons for aesthetics """
        margin = 250
        card = pygame.Rect(margin, 220, self.W - 2 * margin, 430)
        pygame.draw.rect(self.screen, OVERLAY_COLOR, card, border_radius=16)