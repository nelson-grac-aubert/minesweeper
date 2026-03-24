import pygame

from scripts.logic.utils.assets_imports import load_image, load_sound
from scripts.ui.ui_settings import *

class Purchase:

    W, H = 1000, 680

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_back  = pygame.font.SysFont("monospace", 20, bold=True)

        # Thanks message
        raw = load_image("assets/images/thanks.png")
        w, h = raw.get_size()
        self.thanks_img  = pygame.transform.scale(raw, (w * 3, h * 3))
        self.thanks_rect = self.thanks_img.get_rect(center=(self.W // 2, 100))

        # Pigeon Sprite
        raw = load_image("assets/images/pigeon.png")
        w, h = raw.get_size()
        self.pigeon_img  = pygame.transform.scale(raw, (w * 5, h * 5))
        self.pigeon_rect = self.pigeon_img.get_rect(center=(500, 340))

        # Return Button
        back_w, back_h = 160, 50
        self.back_rect = pygame.Rect(
            (self.W - back_w) // 2,
            self.H - back_h - 40,
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
        self.screen.blit(self.thanks_img, self.thanks_rect)
        # Pigeon
        self.screen.blit(self.pigeon_img, self.pigeon_rect)

        # Return button
        hover = self.back_rect.collidepoint(pygame.mouse.get_pos())
        color = ACCENT_COLOR if hover else BACK_COLOR
        pygame.draw.rect(self.screen, color, self.back_rect, border_radius=10)
        label = self.font_back.render("← Retour", True, BG_COLOR if hover else TEXT_COLOR)
        self.screen.blit(label, label.get_rect(center=self.back_rect.center))

    def play_coo(self) : 
        """ Play a pigeon sound """
        coo_coo = load_sound("assets/sounds/coo_coo.mp3")
        coo_coo.play() 