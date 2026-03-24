import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "logic", "utils"))
from scripts.logic.utils.assets_imports import load_image
from scripts.ui.button import Button

import pygame

DIFFICULTIES = ["easy", "medium", "hard"]


class DifficultyButton(Button):
    """Cycle easy → medium → hard au clic gauche."""

    def __init__(self, center: tuple[int, int]):
        self._index  = 0
        self._images: dict[str, pygame.Surface] = {}

        for name in DIFFICULTIES:
            raw = load_image(f"assets/images/{name}.png")
            w, h = raw.get_size()
            self._images[name] = pygame.transform.scale(raw, (w * self.SCALE, h * self.SCALE))

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