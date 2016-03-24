
"""
class: ScreenCapture
"""

import pygame
import pygame.gfxdraw

BACKGROUNDTRANS = (0, 0, 0, 224)       # 1-255 hoger is zwarter


class ScreenCapture(object):
    """
    Maak een schermafdruk en maak het wazig.
    """
    def __init__(self, screen):
        self.screen = screen
        scr_data = pygame.image.tostring(screen, 'RGBA')                            # maak een screen capture
        self.scr_capt = pygame.image.frombuffer(scr_data, screen.get_size(), 'RGBA').convert()
        pygame.gfxdraw.box(self.scr_capt, self.screen.get_rect(), BACKGROUNDTRANS)  # en een doorzichtige laag

    def render(self):
        """
        Teken het op het scherm.
        """
        self.screen.blit(self.scr_capt, (0, 0))
