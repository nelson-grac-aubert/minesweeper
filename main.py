import sys
import pygame

from scripts.ui.home_menu import HomeMenu
from scripts.ui.options   import Options
from scripts.ui.shop  import Shop
from scripts.ui.purchase import Purchase
from scripts.ui.ui_settings import * 

def main() :
    
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption(WINDOW_TITLE)
    clock  = pygame.time.Clock()

    # Menus
    home     = HomeMenu(screen)
    options  = Options(screen)
    shop = Shop(screen)
    purchase = Purchase(screen)

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

            elif current == SCREEN_SHOP:
                action = shop.handle_event(event)

            elif current == SCREEN_PURCHASE : 
                action = purchase.handle_event(event)

            # Transitions between screens
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
                print(f"[main] Nouvelle partie → grille {grid_size}×{grid_size}, {num_bombs} bombes")
                # TODO : instantiate game screen here
                # current = SCREEN_GAME
                # game = Game(screen, grid_size, num_bombs)

        # Draw
        if current == SCREEN_HOME:
            home.draw()
        elif current == SCREEN_OPTIONS:
            options.draw()
        elif current == SCREEN_SHOP:
            shop.draw()
        elif current == SCREEN_PURCHASE:
            purchase.draw()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()