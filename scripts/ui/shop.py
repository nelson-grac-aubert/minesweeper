import pygame

from scripts.logic.utils.assets_imports import load_image
from scripts.ui.button import Button
from scripts.ui.ui_settings import *

class Shop:

    def __init__(self, screen: pygame.Surface):

        self.ads_removed = False
        self.screen = screen
        self.font_back_button  = pygame.font.SysFont("monospace", 20, bold=True)
        self.btn_remove_ads   = Button("assets/images/remove_ads.png", center=(500, 270))
        ads_removed_image = load_image("assets/images/ads_removed.png")
        wi, he = ads_removed_image.get_size()
        self.img_ads_removed  = pygame.transform.scale(ads_removed_image, (wi * 3, he * 3))

        self.flag_button_scale = 1
        self.flag_buttons_y = 450
        self.btn_flag      = Button("assets/images/shop_flag.png",      (250, self.flag_buttons_y), self.flag_button_scale)
        self.btn_blue_flag = Button("assets/images/shop_flag_blue.png", (500, self.flag_buttons_y), self.flag_button_scale)
        self.btn_gold_flag = Button("assets/images/shop_flag_gold.png", (750, self.flag_buttons_y), self.flag_button_scale)

        store_title = load_image("assets/images/store.png")
        w, h = store_title.get_size()
        self.store_img  = pygame.transform.scale(store_title, (w * 3, h * 3))
        self.store_rect = self.store_img.get_rect(center=(WINDOW_W // 2, 100))

        back_w, back_h = 160, 50
        self.back_rect = pygame.Rect(
            (WINDOW_W - back_w) // 2,
            WINDOW_H - back_h - 40,
            back_w, back_h
        )

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.back_rect.collidepoint(event.pos):
                return "back"          # ← était "home", maintenant "back"

            if not self.ads_removed and self.btn_remove_ads.rect.collidepoint(event.pos):
                self.ads_removed = True
                self.btn_remove_ads.image = self.img_ads_removed
                self.btn_remove_ads.rect  = self.img_ads_removed.get_rect(center=(500, 270))
                return "ads purchased"

        return None

    def draw(self) -> None:
        self.screen.fill(BG_COLOR)
        self.btn_remove_ads.draw(self.screen)
        self.btn_flag.draw(self.screen)
        self.btn_blue_flag.draw(self.screen)
        self.btn_gold_flag.draw(self.screen)
        self.screen.blit(self.store_img, self.store_rect)

        hover = self.back_rect.collidepoint(pygame.mouse.get_pos())
        color = ACCENT_COLOR if hover else BACK_COLOR
        pygame.draw.rect(self.screen, color, self.back_rect, border_radius=10)
        label = self.font_back_button.render("← Retour", True, BG_COLOR if hover else TEXT_COLOR)
        self.screen.blit(label, label.get_rect(center=self.back_rect.center))