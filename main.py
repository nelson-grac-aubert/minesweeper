import sys
import pygame

from scripts.ui.home_menu   import HomeMenu
from scripts.ui.options     import Options
from scripts.ui.shop        import Shop
from scripts.ui.purchase    import Purchase
from scripts.ui.game_screen import GameScreen
from scripts.ui.ui_settings import *


def main():

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption(WINDOW_TITLE)
    clock  = pygame.time.Clock()

    # Screens
    home        = HomeMenu(screen)
    options     = Options(screen)
    shop        = Shop(screen)
    purchase    = Purchase(screen)
    game_screen = None

    current = SCREEN_HOME

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            action = None

            if current == SCREEN_HOME:
                action = home.handle_event(event)
            elif current == SCREEN_OPTIONS:
                action = options.handle_event(event)
            elif current == SCREEN_SHOP:
                action = shop.handle_event(event)
            elif current == SCREEN_PURCHASE:
                action = purchase.handle_event(event)
            elif current == SCREEN_GAME and game_screen:
                action = game_screen.handle_event(event)

            # Transitions
            if action == "options":
                current = SCREEN_OPTIONS

            elif action == "shop":
                current = SCREEN_SHOP

            elif action == "home":
                current = SCREEN_HOME

            elif action == "ads purchased":
                purchase.play_coo()
                home.ads_removed = True
                current = SCREEN_PURCHASE

            elif isinstance(action, tuple) and action[0] == "new_game":
                _, grid_size, num_bombs = action
                difficulty  = home.btn_difficulty.current  # "easy" | "medium" | "hard"
                game_screen = GameScreen(screen, grid_size, num_bombs, difficulty)
                current     = SCREEN_GAME

        # Render
        if current == SCREEN_HOME:
            home.draw()
        elif current == SCREEN_OPTIONS:
            options.draw()
        elif current == SCREEN_SHOP:
            shop.draw()
        elif current == SCREEN_PURCHASE:
            purchase.draw()
        elif current == SCREEN_GAME and game_screen:
            game_screen.draw()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()