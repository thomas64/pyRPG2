
"""
class: SellBox
"""

import pygame

COLORKEY = pygame.Color("purple")
LINECOLOR = pygame.Color("black")

FONTCOLOR = pygame.Color("white")
FONT = 'impact'
LARGEFONTSIZE = 25
NORMALFONTSIZE = 15


class SellBox(object):
    """
    ...
    """
    def __init__(self, x, y, width, height):
        self.surface = pygame.Surface((width, height))
        self.surface.fill(COLORKEY)
        self.surface.set_colorkey(COLORKEY)
        self.surface = self.surface.convert()

        self.rect = self.surface.get_rect()
        self.rect.topleft = x, y

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

        pygame.draw.rect(self.surface, LINECOLOR, self.surface.get_rect(), 1)

    def render(self, screen):
        """
        :param screen:
        """

        screen.blit(self.surface, self.rect.topleft)
