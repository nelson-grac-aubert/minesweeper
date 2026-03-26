import pygame

from scripts.logic.utils.assets_imports import load_image
from scripts.ui.button import Button
from scripts.ui.ui_settings import *

class Shop:

    def __init__(self, screen: pygame.Surface):

        self.ads_removed    = False
        self.blue_purchased = False
        self.gold_purchased = False

        self.screen = screen

        # Button remove ads
        self.btn_remove_ads   = Button("assets/images/remove_ads.png", center=(500, 270))
        ads_removed_image = load_image("assets/images/ads_removed.png")
        wi, he = ads_removed_image.get_size()
        self.img_ads_removed  = pygame.transform.scale(ads_removed_image, (wi * 4, he * 4))

        self.flag_button_scale = 1
        self.flag_buttons_y = 450
        self.btn_flag      = Button("assets/images/shop_flag.png",      (250, self.flag_buttons_y), self.flag_button_scale)
        self.btn_blue_flag = Button("assets/images/shop_flag_blue.png", (500, self.flag_buttons_y), self.flag_button_scale)
        self.btn_gold_flag = Button("assets/images/shop_flag_gold.png", (750, self.flag_buttons_y), self.flag_button_scale)

        # "Obtenu" badge surface on flag skins
        badge_img = load_image("assets/images/bought.png")
        bw, bh = badge_img.get_size()
        self.badge_img = pygame.transform.scale(badge_img, (bw * 1.5, bh * 1.5)) 
        self.badge_rect = self.badge_img.get_rect()

        # Icon shop
        store_title = load_image("assets/images/store.png")
        w, h = store_title.get_size()
        self.store_img  = pygame.transform.scale(store_title, (w * 3, h * 3))
        self.store_rect = self.store_img.get_rect(center=(WINDOW_W // 2, 100))

        # Back button rectangle (position reference)
        back_w, back_h = 160, 50
        self.back_rect = pygame.Rect(
            (WINDOW_W - back_w) // 2,
            WINDOW_H - back_h - 40,
            back_w, back_h
        )

        # Back button sprite
        self.back_button = Button("assets/images/return_button.png",
                                center=self.back_rect.center)


    def mark_purchased(self, skin: str) -> None:
        """Called by main after purchase confirmation."""
        if skin == "blue":
            self.blue_purchased = True
        elif skin == "gold":
            self.gold_purchased = True

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.back_button.rect.collidepoint(event.pos):
                return "back"

            if not self.ads_removed and self.btn_remove_ads.rect.collidepoint(event.pos):
                self.ads_removed = True
                self.btn_remove_ads.image = self.img_ads_removed
                self.btn_remove_ads.rect  = self.img_ads_removed.get_rect(center=(500, 270))
                return "ads purchased"

            # Blue flag — first click triggers purchase screen
            if not self.blue_purchased and self.btn_blue_flag.rect.collidepoint(event.pos):
                return ("flag_purchased", "blue")

            # Gold flag — first click triggers purchase screen
            if not self.gold_purchased and self.btn_gold_flag.rect.collidepoint(event.pos):
                return ("flag_purchased", "gold")

        return None

    def draw(self) -> None:
        self.screen.fill(BG_COLOR)
        self.btn_remove_ads.draw(self.screen)

        # Default flag (always available — no purchase needed)
        self.btn_flag.draw(self.screen)

        # Blue flag
        self.btn_blue_flag.draw(self.screen)
        if self.blue_purchased:
            rect = self.badge_img.get_rect(
                centerx=self.btn_blue_flag.rect.centerx,
                top=self.btn_blue_flag.rect.bottom
            )
            self.screen.blit(self.badge_img, rect)

        # Gold flag
        self.btn_gold_flag.draw(self.screen)
        if self.gold_purchased:
            rect = self.badge_img.get_rect(
                centerx=self.btn_gold_flag.rect.centerx,
                top=self.btn_gold_flag.rect.bottom
            )
            self.screen.blit(self.badge_img, rect)

        # Title
        self.screen.blit(self.store_img, self.store_rect)

        # Return Button
        self.back_button.draw(self.screen)
