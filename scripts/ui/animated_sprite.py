import os
import pygame
from scripts.logic.utils.assets_imports import resource_path, load_image

class AnimatedSprite:
    """ A class to manage several frames of animation as Pygame doesn't support gifs directly """
    def __init__(self, folder_path: str, frame_rate: int = 10, scale:int = 1):
        self.frames = []
        self.index = 0
        self.timer = 0
        self.scale = scale
        self.frame_rate = frame_rate  # frames per second

        # Load all PNG frames from the folder
        for filename in sorted(os.listdir(resource_path(folder_path))):
            if filename.endswith(".png"):
                full = os.path.join(folder_path, filename)
                img = load_image(full)

                # Apply scaling if needed
                if scale != 1:
                    w = img.get_width() * scale
                    h = img.get_height() * scale
                    img = pygame.transform.scale(img, (w, h))

                self.frames.append(img)

        self.image = self.frames[0]

    def update(self, dt):
        """ Change the frame of the animation """
        self.timer += dt
        if self.timer >= 1 / self.frame_rate:
            self.timer = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]

    def draw_centered(self, screen, center):
        """Draw the current frame centered on the given (x, y) position."""
        rect = self.image.get_rect(center=center)
        screen.blit(self.image, rect)


    
