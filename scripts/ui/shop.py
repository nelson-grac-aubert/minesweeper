import pygame
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "logic", "utils"))
from scripts.logic.utils.assets_imports import load_image
from scripts.ui.button import Button

BG_COLOR     = (30,  30,  46)
TEXT_COLOR   = (205, 214, 244)
ACCENT_COLOR = (166, 227, 161) 
BACK_COLOR   = (49,  50,  68)


class Shop:

    W, H = 1000, 680

    def __init__(self, screen: pygame.Surface):

        self.ads_removed = False
        self.screen = screen
        # Back button font
        self.font_back_button  = pygame.font.SysFont("monospace", 20, bold=True)
        # Button remove ads
        self.btn_remove_ads   = Button("assets/images/remove_ads.png", center=(500, 270))
        # Button ads removed
        ads_removed_image = load_image("assets/images/ads_removed.png")
        wi, he = ads_removed_image.get_size()
        self.img_ads_removed  = pygame.transform.scale(ads_removed_image, (wi * 3, he * 3))

        # Button buy flag skin
        self.flag_button_scale = 1
        self.flag_buttons_y = 450
        self.btn_flag = Button("assets/images/shop_flag.png", (250, self.flag_buttons_y), self.flag_button_scale)
        self.btn_blue_flag = Button("assets/images/shop_flag_blue.png", (500, self.flag_buttons_y), self.flag_button_scale)
        self.btn_gold_flag = Button("assets/images/shop_flag_gold.png", (750, self.flag_buttons_y), self.flag_button_scale)

        # Icon shop
        store_title = load_image("assets/images/store.png")
        w, h = store_title.get_size()
        self.store_img  = pygame.transform.scale(store_title, (w * 3, h * 3))
        self.store_rect = self.store_img.get_rect(center=(self.W // 2, 100))

        # Return Button
        back_w, back_h = 160, 50
        self.back_rect = pygame.Rect(
            (self.W - back_w) // 2,
            self.H - back_h - 40,
            back_w, back_h
        )

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Button back to main menu
            if self.back_rect.collidepoint(event.pos):
                return "home"
            
            # Button remove adds
            if not self.ads_removed and self.btn_remove_ads.rect.collidepoint(event.pos):
                self.ads_removed = True
                self.btn_remove_ads.image = self.img_ads_removed
                self.btn_remove_ads.rect  = self.img_ads_removed.get_rect(center=(500, 270))
                return "remove_ads"
        return None

    def draw(self) -> None:
        self.screen.fill(BG_COLOR)

        # Button remove ads
        self.btn_remove_ads.draw(self.screen)

        # Button buy flags
        self.btn_flag.draw(self.screen)
        self.btn_blue_flag.draw(self.screen)
        self.btn_gold_flag.draw(self.screen)

        # Title
        self.screen.blit(self.store_img, self.store_rect)

        # Return button
        hover = self.back_rect.collidepoint(pygame.mouse.get_pos())
        color = ACCENT_COLOR if hover else BACK_COLOR
        pygame.draw.rect(self.screen, color, self.back_rect, border_radius=10)
        label = self.font_back_button.render("← Retour", True, BG_COLOR if hover else TEXT_COLOR)
        self.screen.blit(label, label.get_rect(center=self.back_rect.center))