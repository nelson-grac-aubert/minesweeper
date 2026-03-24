import pygame
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "logic", "utils"))
from scripts.logic.utils.assets_imports import load_image


class Button:
    """Bouton cliquable à partir d'une image PNG scalée."""

    SCALE = 3  # zoom factor for pixel art assets

    def __init__(self, image_path: str, center: tuple[int, int]):
        raw = load_image(image_path)
        w, h = raw.get_size()
        self.image = pygame.transform.scale(raw, (w * self.SCALE, h * self.SCALE))
        self.rect  = self.image.get_rect(center=center)

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