import sys
import pygame

from scripts.ui.home_menu   import HomeMenu
from scripts.ui.options     import Options
from scripts.ui.shop        import Shop
from scripts.ui.purchase    import Purchase
from scripts.ui.game_screen import GameScreen
from scripts.ui.ui_settings import *

def init_game():
    """ Initialize Pygame, variables, game states"""

    # Pygame init
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    # UI Screens
    screens = {
        SCREEN_HOME:     HomeMenu(screen),
        SCREEN_OPTIONS:  Options(screen),
        SCREEN_SHOP:     Shop(screen),
        SCREEN_PURCHASE: Purchase(screen),
        SCREEN_GAME:     None
    }

    # Global state
    state = {
        "current": SCREEN_HOME,
        "previous": SCREEN_HOME,
        "unlocked_skins": ["default"],
        "ads_removed": False,
        "game_screen": None
    }

    return screen, clock, screens, state

def handle_events(current, screens, state):
    """ Return an action string or tuple, or None. """
    for event in pygame.event.get():

        # Quit window with red cross
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Listen to events of the current screen (see its own script for .handle_event() method)
        screen_obj = screens[current] if current != SCREEN_GAME else state["game_screen"]
        if screen_obj:
            action = screen_obj.handle_event(event)
            if action:
                return action

    return None

def apply_actions(action, screens, state):

    if action is None:
        return

    current = state["current"]

    # Simple transitions
    if action == "options":
        state["current"] = SCREEN_OPTIONS

    elif action == "shop":
        state["previous"] = current
        state["current"] = SCREEN_SHOP

    elif action == "home":
        state["current"] = SCREEN_HOME

    elif action == "back":
        if state["previous"] == SCREEN_GAME:
            state["game_screen"].resume()
            state["current"] = SCREEN_GAME
        else:
            state["current"] = SCREEN_HOME

    # Ads purchased
    elif action == "ads purchased":
        state["ads_removed"] = True
        screens[SCREEN_PURCHASE].play_coo()
        screens[SCREEN_HOME].ads_removed = True
        if state["game_screen"]:
            state["game_screen"].ads_removed = True
        state["current"] = SCREEN_PURCHASE

    # Skin purchased
    elif action[0] == "flag_purchased":
        skin = action[1]
        if skin not in state["unlocked_skins"]:
            state["unlocked_skins"].append(skin)
        screens[SCREEN_SHOP].mark_purchased(skin)
        screens[SCREEN_PURCHASE].play_coo()
        state["current"] = SCREEN_PURCHASE

    # New game
    elif action[0] == "new_game":
        new_game, grid_size, num_bombs = action
        print(action)
        difficulty = screens[SCREEN_HOME].btn_difficulty.current

        state["game_screen"] = GameScreen(
            screens[SCREEN_HOME].screen,
            grid_size, num_bombs, difficulty,
            state["unlocked_skins"],
            state["ads_removed"]
        )

        state["current"] = SCREEN_GAME

def draw(current, screens, state, dt, dt_ms):
    """ Draw all elements of the current screen state on the window """

    if current == SCREEN_HOME:
        screens[SCREEN_HOME].draw()
        screens[SCREEN_HOME].left_coin.update(dt)
        screens[SCREEN_HOME].right_coin.update(dt)

    elif current == SCREEN_OPTIONS:
        screens[SCREEN_OPTIONS].draw()

    elif current == SCREEN_SHOP:
        screens[SCREEN_SHOP].draw()

    elif current == SCREEN_PURCHASE:
        screens[SCREEN_PURCHASE].draw()

    elif current == SCREEN_GAME :
        state["game_screen"].update(dt_ms)
        state["game_screen"].draw()

    pygame.display.flip()

def main():

    screen, clock, screens, state = init_game()

    while True:
        dt_ms = clock.tick(FPS)
        dt = dt_ms / 1000

        action = handle_events(state["current"], screens, state)  

        apply_actions(action, screens, state)

        draw(state["current"], screens, state, dt, dt_ms)


if __name__ == "__main__":

    main()