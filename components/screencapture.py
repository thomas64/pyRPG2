
"""
class: ScreenCapture
"""

import pygame
import pygame.gfxdraw

BACKGROUNDTRANS = (0, 0, 0, 224)       # 1-255 hoger is zwarter
BACKGROUNDCOLOR = pygame.Color("black")


class ScreenCapture(object):
    """
    Maak een schermafdruk en maak het wazig.
    """
    def __init__(self, black_background=False):
        self.screen = pygame.display.get_surface()
        scr_data = pygame.image.tostring(self.screen, 'RGBA')                       # maak een screen capture

        if black_background:
            self.image = pygame.Surface(self.screen.get_size())
            self.image.fill(BACKGROUNDCOLOR)
        else:
            self.image = pygame.image.frombuffer(scr_data, self.screen.get_size(), 'RGBA').convert()
            pygame.gfxdraw.box(self.image, self.screen.get_rect(), BACKGROUNDTRANS)     # en een doorzichtige laag

    def render(self):
        """
        Teken het op het scherm.
        """
        self.screen.blit(self.image, (0, 0))
