import pygame

from scripts.logic.utils.assets_imports import load_image
from scripts.ui.button import Button
from scripts.ui.ui_settings import *

class Options:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        # Icon options
        raw = load_image("assets/images/options.png")
        w, h = raw.get_size()
        self.options_img  = pygame.transform.scale(raw, (w * 4, h * 4))
        self.options_rect = self.options_img.get_rect(center=(WINDOW_W // 2, 75))

        # Back button rectangle (position reference)
        back_w, back_h = 160, 50
        self.back_rect = pygame.Rect(
            (WINDOW_W - back_w) // 2,
            WINDOW_H - back_h - 40,
            back_w, back_h
        )

        # Back button sprite
        self.back_button = Button("assets/images/return_button.png",
                                center=self.back_rect.center)

    def handle_event(self, event: pygame.event.Event):
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.back_rect.collidepoint(event.pos)
        ):
            return "home"
        return None

    def draw(self) -> None:
        self.screen.fill(BG_COLOR)

        # Title 
        self.screen.blit(self.options_img, self.options_rect)

        # Return Button
        self.back_button.draw(self.screen)