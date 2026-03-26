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

    home        = HomeMenu(screen)
    options     = Options(screen)
    shop        = Shop(screen)
    purchase    = Purchase(screen)
    game_screen = None

    current       = SCREEN_HOME
    previous      = SCREEN_HOME   # ← memorizes the screen before the shop
    # Skins
    unlocked_skins = ["default"]

    current = SCREEN_HOME

    while True:

        dt_ms = clock.tick(FPS)          # microseconds
        dt    = dt_ms / 1000             # seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            action = None

            # What events are listened to depending on screen
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
                previous = current          # Remembers what screen was before (game or menu)
                current  = SCREEN_SHOP

            elif action == "home":
                current = SCREEN_HOME

            elif action == "back":
                # Back from shop
                if previous == SCREEN_GAME and game_screen:
                    game_screen.resume()    # Resume timer
                    current = SCREEN_GAME
                else:
                    current = SCREEN_HOME

            elif action == "ads purchased":
                purchase.play_coo()
                home.ads_removed = True
                current = SCREEN_PURCHASE

            elif isinstance(action, tuple) and action[0] == "flag_purchased":
                skin = action[1]
                if skin not in unlocked_skins:
                    unlocked_skins.append(skin)
                shop.mark_purchased(skin)
                purchase.play_coo()
                current = SCREEN_PURCHASE
 
            elif isinstance(action, tuple) and action[0] == "new_game":
                _, grid_size, num_bombs = action
                difficulty  = home.btn_difficulty.current  # "easy" | "medium" | "hard"
                game_screen = GameScreen(screen, grid_size, num_bombs, difficulty, unlocked_skins)
                current     = SCREEN_GAME

        # rendering

        if current == SCREEN_HOME:
            home.draw()
            home.left_coin.update(dt)
            home.right_coin.update(dt)
        elif current == SCREEN_OPTIONS:
            options.draw()
        elif current == SCREEN_SHOP:
            shop.draw()
        elif current == SCREEN_PURCHASE:
            purchase.draw()
        elif current == SCREEN_GAME and game_screen:
            game_screen.update(dt_ms)   # Animate ad
            game_screen.draw()

        pygame.display.flip()


if __name__ == "__main__":
    main()