import pygame

from scripts.logic.utils.assets_imports import load_image
from scripts.ui.ui_settings import *

class GameScreen:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_back = pygame.font.SysFont("monospace", 20, bold=True)

        # Title icon
        raw = load_image("assets/images/title.png")
        w, h = raw.get_size()
        self.title_img = pygame.transform.scale(raw, (w * 3, h * 3))
        self.title_rect = self.title_img.get_rect(center=(WINDOW_W // 2, 50))

        # Return Button
        back_w, back_h = 160, 50
        self.back_rect = pygame.Rect(
            (WINDOW_W - back_w) // 2,
            WINDOW_H - back_h - 40,
            back_w, back_h
        )

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
        self.screen.blit(self.title_img, self.title_rect)

        # Return button
        hover = self.back_rect.collidepoint(pygame.mouse.get_pos())
        color = ACCENT_COLOR if hover else BACK_COLOR
        pygame.draw.rect(self.screen, color, self.back_rect, border_radius=10)
        label = self.font_back.render("← Retour", True, BG_COLOR if hover else TEXT_COLOR)
        self.screen.blit(label, label.get_rect(center=self.back_rect.center))