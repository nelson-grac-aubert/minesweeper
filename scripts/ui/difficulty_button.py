from scripts.logic.utils.assets_imports import load_image
from scripts.ui.button import Button

import pygame

DIFFICULTIES = ["easy", "medium", "hard"]


class DifficultyButton(Button):
    """Cycle easy → medium → hard on left click"""

    def __init__(self, center: tuple[int, int], scale = 3):
        self._index  = 0
        self.scale = scale
        self._images: dict[str, pygame.Surface] = {}

        for name in DIFFICULTIES:
            raw = load_image(f"assets/images/{name}.png")
            w, h = raw.get_size()
            self._images[name] = pygame.transform.scale(raw, (w * self.scale, h * self.scale))

        self.image = self._images["easy"]
        self.rect  = self.image.get_rect(center=center)
        self._hover_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self._hover_surf.fill((255, 255, 255, 40))

    @property
    def current(self) -> str:
        return DIFFICULTIES[self._index]

    def cycle(self) -> None:
        self._index = (self._index + 1) % len(DIFFICULTIES)
        old_center = self.rect.center
        self.image = self._images[self.current]
        self.rect = self.image.get_rect(center=old_center)

        # Recreate hover surface with new sprite size
        self._hover_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self._hover_surf.fill((255, 255, 255, 40))


    def is_clicked(self, event: pygame.event.Event) -> bool:
        clicked = super().is_clicked(event)
        if clicked:
            self.cycle()
        return clicked