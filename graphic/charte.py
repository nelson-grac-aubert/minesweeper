#chartre graphique pygame 
import pygame
import json


class CharteGraphique:
    def __init__(self):
        self.colors = {
            "background": (255, 255, 255),
            "text": (0, 0, 0),
            "button": (200, 200, 200),
            "button_hover": (150, 150, 150),
            "button_text": (0, 0, 0)
        }
        self.fonts = {
            "default": pygame.font.SysFont("Arial", 24),
            "title": pygame.font.SysFont("Arial", 36)
        }
        #toute les couleurs de pygame sont stocké dans un disctionnaire pour faliciter leur utilisation dans le code

        def get_color(self, name):
            return self.colors.get(name, (0, 0, 0))
        #fonction pour recuperer une couleur par son nom
        def get_font(self, name):
            return self.fonts.get(name, pygame.font.SysFont("Arial", 24))
        #fonction pour recuperer une police par son nom
        def get_police(self,name):
            return self.fonts.get(name,pygame.font.SysFont("Arial",24))
        
