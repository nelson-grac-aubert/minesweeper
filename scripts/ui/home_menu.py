import pygame
import random
import webbrowser

from scripts.ui.button            import Button
from scripts.ui.difficulty_button import DifficultyButton
from scripts.logic.utils.assets_imports import load_music
from scripts.ui.ui_settings import *
from scripts.ui.title_coins import *



DIFFICULTY_PARAMS = {
    "easy":   {"grid": 8,  "bombs_min": 15,  "bombs_max": 20},
    "medium": {"grid": 10, "bombs_min": 20,  "bombs_max": 30},
    "hard":   {"grid": 12, "bombs_min": 100, "bombs_max": 120},
}


class HomeMenu:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        screen_center_x = WINDOW_W // 2

        # Music

        self.play_pink_floyd()

        # Title
        from scripts.logic.utils.assets_imports import load_image
        raw_title = load_image("assets/images/title.png")
        tw, th    = raw_title.get_size()
        self.title_img  = pygame.transform.scale(raw_title, (tw * 5, th * 5))
        self.title_rect = self.title_img.get_rect(center=(screen_center_x, 100))

        # Coins 
        self.left_coin, self.right_coin = load_title_coin_animations()
        self.left_coin_rect, self.right_coin_rect = position_title_coins(self.title_rect)


        # Buttons
        self.btn_new_game   = Button("assets/images/new_game.png", center=(screen_center_x, 270))
        self.btn_difficulty = DifficultyButton(center=(screen_center_x, 360))
        self.btn_options    = Button("assets/images/options.png",  center=(screen_center_x, 450))
        self.btn_shop       = Button("assets/images/store.png",    center=(screen_center_x, 560))

        # Ads
        self.ads_removed = False
        fruit_ad = load_image("assets/images/fruit_ad.png")
        pokemon_ad = load_image("assets/images/pokemon_ad.png")
        ad_w, ad_h = fruit_ad.get_size() 
        self.fruit_img = pygame.transform.scale(fruit_ad, (ad_w * 1.3, ad_h * 1.3))
        self.pokemon_img = pygame.transform.scale(pokemon_ad, (ad_w * 1.3, ad_h * 1.3))

        # Ads position
        self.ad_left_rect  = self.fruit_img.get_rect(midleft=(40, WINDOW_H // 2 + 100))
        self.ad_right_rect = self.pokemon_img.get_rect(midright=(WINDOW_W - 40, WINDOW_H // 2 + 100))


    def handle_event(self, event: pygame.event.Event):
        # Change difficulty
        if self.btn_difficulty.is_clicked(event):
            return None

        # Start New Game
        if self.btn_new_game.is_clicked(event):
            diff   = self.btn_difficulty.current
            params = DIFFICULTY_PARAMS[diff]
            bombs  = random.randint(params["bombs_min"], params["bombs_max"])
            return ("new_game", params["grid"], bombs)
        
        # Ad
        if not self.ads_removed and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.ad_left_rect.collidepoint(event.pos):
                webbrowser.open("https://github.com/nelson-grac-aubert/fruit-slicer/releases")
                return None
            elif self.ad_right_rect.collidepoint(event.pos):
                webbrowser.open("https://github.com/ceciliaperana13/pokemon_")
                return None

        # Click Options
        if self.btn_options.is_clicked(event):
            return "options"

        # Click Shop
        if self.btn_shop.is_clicked(event):
            return "shop"

        return None

    def draw(self) -> None:
        self.screen.fill(BG_COLOR)
        self._draw_card()
        self.screen.blit(self.title_img, self.title_rect)
        self.btn_new_game.draw(self.screen)
        self.btn_difficulty.draw(self.screen)
        self.btn_options.draw(self.screen)
        self.btn_shop.draw(self.screen)

        # Ads
        if not self.ads_removed:
            self.screen.blit(self.fruit_img, self.ad_left_rect)
            self.screen.blit(self.pokemon_img, self.ad_right_rect)
        
        # Coins 
        draw_title_coins(self.screen,self.left_coin,self.right_coin,self.left_coin_rect,self.right_coin_rect)


    def _draw_card(self) -> None:
        margin = 250
        card = pygame.Rect(margin, 220, WINDOW_W - 2 * margin, 430)
        pygame.draw.rect(self.screen, OVERLAY_COLOR, card, border_radius=16)

    def play_pink_floyd(self) : 
        """ Play Money by Pink Floyd on launch"""

        load_music("assets/music/money_pink_floyd.mp3")
        pygame.mixer.music.play(-1)