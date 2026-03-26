# Bannière publicitaire fictive pour MicrotransacMines.
# Usage : AdBanner(screen, x, y, width, height) puis .update() + .draw() chaque frame.

import pygame
import random
import math


# données fictives

ADS = [
    {
        "brand":   "BOMBA™",
        "tagline": "L'énergie qui te fait exploser",
        "sub":     "Boisson énergisante • Nouveau goût Uranium",
        "bg":      (20,  20,  40),
        "accent":  (255, 80,  0),
        "badge":   "PROMO -50%",
    },
    {
        "brand":   "MineCoins",
        "tagline": "Achète des vraies mines virtuelles",
        "sub":     "Pack Starter : 99,99 € — offre limitée",
        "bg":      (10,  30,  10),
        "accent":  (0,   220, 80),
        "badge":   "HOT DEAL",
    },
    {
        "brand":   "SafeGuard Pro",
        "tagline": "Détecteur de mines IA — 3 essais gratuits",
        "sub":     "Abonnement mensuel • Annulable jamais",
        "bg":      (30,  10,  40),
        "accent":  (180, 60,  255),
        "badge":   "NOUVEAU",
    },
    {
        "brand":   "FlagMaster 9000",
        "tagline": "Pose ton drapeau. Pose-le mieux.",
        "sub":     "5 étoiles  —  2 acheteurs satisfaits",
        "bg":      (40,  20,  10),
        "accent":  (255, 200, 0),
        "badge":   "TOP VENTE",
    },
    {
        "brand":   "CryptoMine™",
        "tagline": "Miner sans risque… ou presque",
        "sub":     "Investis dans le vide numérique dès 5 €",
        "bg":      (10,  25,  35),
        "accent":  (0,   190, 255),
        "badge":   "100% LÉGAL",
    },
]


#  classe principale

class AdBanner:
    """
    Bannière publicitaire animée avec transition en slide gauche/droite.

    Paramètres
    ----------
    screen  : pygame.Surface cible
    x, y    : position sur l'écran
    width   : largeur de la bannière
    height  : hauteur de la bannière
    """

    ROTATE_MS  = 4000   # durée d'affichage d'une pub (ms)
    ANIM_MS    = 350    # durée du slide (ms)

    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.rect   = pygame.Rect(x, y, width, height)

        # Surfaces internes
        self._surf_a = pygame.Surface((width, height), pygame.SRCALPHA)
        self._surf_b = pygame.Surface((width, height), pygame.SRCALPHA)

        # Clip rect pour masquer ce qui dépasse pendant le slide
        self._clip = pygame.Rect(x, y, width, height)

        # État
        self._ads           = ADS[:]
        random.shuffle(self._ads)
        self._idx           = 0
        self._t             = 0        # ms depuis dernier changement
        self._transitioning = False
        self._slide_x       = 0.0     # décalage horizontal courant (pixels, float)

        # Polices
        self._font_brand   = pygame.font.SysFont("consolas", height // 3, bold=True)
        self._font_tagline = pygame.font.SysFont("consolas", height // 5)
        self._font_sub     = pygame.font.SysFont("consolas", max(10, height // 7))
        self._font_badge   = pygame.font.SysFont("consolas", max(9,  height // 6), bold=True)

        # Rendu initial
        self._render(self._surf_a, self._current_ad())
        self._render(self._surf_b, self._next_ad())

        # Particules (petits pixels animés)
        self._particles = [
            [random.randint(0, width), random.randint(0, height),
             random.uniform(-0.3, 0.3), random.uniform(-0.2, 0.2),
             random.randint(2, 4)]
            for _ in range(18)
        ]

    # ── accès ────────────────────────────────────────────────────────────────

    def _current_ad(self):
        return self._ads[self._idx % len(self._ads)]

    def _next_ad(self):
        return self._ads[(self._idx + 1) % len(self._ads)]

    # ── ease ─────────────────────────────────────────────────────────────────

    @staticmethod
    def _ease_in_out(t: float) -> float:
        """Courbe cubique ease-in-out pour un slide fluide."""
        return t * t * (3.0 - 2.0 * t)

    # ── rendu d'une pub ───────────────────────────────────────────────────────

    def _render(self, surf, ad):
        surf.fill(ad["bg"])
        w, h = surf.get_size()
        ac   = ad["accent"]

        # Bande décorative gauche
        pygame.draw.rect(surf, ac, (0, 0, 6, h))

        # Bande décorative droite
        pygame.draw.rect(surf, ac, (w - 6, 0, 6, h))

        # Ligne horizontale basse
        pygame.draw.line(surf, ac, (6, h - 4), (w - 6, h - 4), 2)

        # Nom de marque
        brand_surf = self._font_brand.render(ad["brand"], True, ac)
        surf.blit(brand_surf, (16, h // 2 - brand_surf.get_height() // 2 - 6))

        # Tagline
        tag_surf = self._font_tagline.render(ad["tagline"], True, (220, 220, 220))
        surf.blit(tag_surf, (16, h // 2 + brand_surf.get_height() // 2 - 4))

        # Sous-texte
        sub_surf = self._font_sub.render(ad["sub"], True, (140, 140, 140))
        surf.blit(sub_surf, (16, h - sub_surf.get_height() - 8))

        # Badge (coin droit)
        badge_surf = self._font_badge.render(ad["badge"], True, ad["bg"])
        pad = 6
        bw  = badge_surf.get_width()  + pad * 2
        bh  = badge_surf.get_height() + pad
        pygame.draw.rect(surf, ac, (w - bw - 12, 8, bw, bh), border_radius=4)
        surf.blit(badge_surf, (w - bw - 12 + pad, 8 + pad // 2))

        # Petit bouton "Fermer" (fictif)
        close_surf = self._font_sub.render("✕", True, (80, 80, 80))
        surf.blit(close_surf, (w - close_surf.get_width() - 4, h - close_surf.get_height() - 4))

    # ── update / draw ─────────────────────────────────────────────────────────

    def update(self, dt_ms):
        """Appeler chaque frame avec le delta-time en millisecondes."""
        self._t += dt_ms
        w = self.rect.width

        # Anime les particules
        h = self.rect.height
        for p in self._particles:
            p[0] += p[2]
            p[1] += p[3]
            if p[0] < 0 or p[0] > w:
                p[2] *= -1
            if p[1] < 0 or p[1] > h:
                p[3] *= -1

        # Déclenchement du slide
        if not self._transitioning and self._t >= self.ROTATE_MS:
            self._transitioning = True
            self._t             = 0
            self._slide_x       = 0.0

        # Animation slide
        if self._transitioning:
            progress      = min(self._t / self.ANIM_MS, 1.0)
            eased         = self._ease_in_out(progress)
            self._slide_x = eased * w          # surf_a part vers la gauche

            if progress >= 1.0:
                # Transition terminée : on avance
                self._idx          += 1
                self._slide_x       = 0.0
                self._transitioning = False
                self._t             = 0
                self._render(self._surf_a, self._current_ad())
                self._render(self._surf_b, self._next_ad())

    def draw(self):
        """Dessine la bannière sur le screen fourni à l'init."""
        w = self.rect.width
        ox, oy = self.rect.topleft

        # Activer le clipping pour que les surfaces ne débordent pas
        old_clip = self.screen.get_clip()
        self.screen.set_clip(self._clip)

        if self._transitioning:
            # surf_a glisse vers la gauche
            self.screen.blit(self._surf_a, (ox - int(self._slide_x), oy))
            # surf_b arrive depuis la droite
            self.screen.blit(self._surf_b, (ox + w - int(self._slide_x), oy))
        else:
            self.screen.blit(self._surf_a, (ox, oy))

        # Restaurer le clip
        self.screen.set_clip(old_clip)

        # Particules par-dessus (dans la zone clippée à la main)
        ad = self._current_ad()
        for p in self._particles:
            px = int(ox + p[0])
            py = int(oy + p[1])
            if self._clip.collidepoint(px, py):
                pygame.draw.circle(self.screen, ad["accent"], (px, py), p[4], 1)

        # Bordure externe
        pygame.draw.rect(self.screen, ad["accent"], self.rect, 2)