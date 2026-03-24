import sys
import os
import pygame

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from scripts.ui.home_menu import HomeMenu
from scripts.ui.options   import Options
from scripts.ui.shop  import Shop


# CONSTANTS
WINDOW_W, WINDOW_H = 1000, 680
FPS                = 60
WINDOW_TITLE       = "MICROTRANSACMINE"


# SCREENS
SCREEN_HOME = "home"
SCREEN_OPTIONS  = "options"
SCREEN_shop = "shop"
SCREEN_GAME     = "game"     # Adrien et Cécilia


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption(WINDOW_TITLE)
    clock  = pygame.time.Clock()

    # Menus
    home     = HomeMenu(screen)
    options  = Options(screen)
    shop = Shop(screen)

    current = SCREEN_HOME

    # Main Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Current screen events
            action = None

            if current == SCREEN_HOME:
                action = home.handle_event(event)

            elif current == SCREEN_OPTIONS:
                action = options.handle_event(event)

            elif current == SCREEN_shop:
                action = shop.handle_event(event)

            # Transitions between screens
            if action == "options":
                current = SCREEN_OPTIONS

            elif action == "shop":
                current = SCREEN_shop

            elif action == "home":
                current = SCREEN_HOME

            elif isinstance(action, tuple) and action[0] == "new_game":
                _, grid_size, num_bombs = action
                print(f"[main] Nouvelle partie → grille {grid_size}×{grid_size}, {num_bombs} bombes")
                # TODO : instancier et lancer l'écran de jeu ici
                # current = SCREEN_GAME
                # game = Game(screen, grid_size, num_bombs)

        # Draw
        if current == SCREEN_HOME:
            home.draw()
        elif current == SCREEN_OPTIONS:
            options.draw()
        elif current == SCREEN_shop:
            shop.draw()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()