import pygame
from scripts.logic.utils.assets_imports import resource_path
from scripts.ui.animated_sprite import AnimatedSprite


def load_title_coin_animations(frame_rate: int = 12):
    """Load 2 coins animations"""

    left_coin  = AnimatedSprite("assets/images/coin",  frame_rate, 5)
    right_coin = AnimatedSprite("assets/images/coin", frame_rate, 5)

    return left_coin, right_coin


def position_title_coins(title_rect: pygame.Rect, offset: int = 60):
    """Calculate position around title"""

    left_rect = pygame.Rect(0, 0, 0, 0)
    right_rect = pygame.Rect(0, 0, 0, 0)

    # On place les coins autour du titre
    left_rect.midright  = (title_rect.left - offset,  title_rect.centery)
    right_rect.midleft  = (title_rect.right + offset, title_rect.centery)

    return left_rect, right_rect


def update_title_coins(left_coin: AnimatedSprite,
                       right_coin: AnimatedSprite,
                       dt: float):
    """Update animation"""
    left_coin.update(dt)
    right_coin.update(dt)


def draw_title_coins(screen: pygame.Surface,
                     left_coin: AnimatedSprite,
                     right_coin: AnimatedSprite,
                     left_rect: pygame.Rect,
                     right_rect: pygame.Rect):
    """Draws animated coins around title"""
    left_coin.draw_centered(screen, left_rect.center)
    right_coin.draw_centered(screen, right_rect.center)