import pygame

from scripts.logic.utils.assets_imports import load_image

class Button:
    """Clickable button from a scale PNG image"""

    def __init__(self, image_path: str, center: tuple[int, int], scale = 3):
        raw = load_image(image_path)
        w, h = raw.get_size()
        self.scale = scale
        self.image = pygame.transform.scale(raw, (w * self.scale, h * self.scale))
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