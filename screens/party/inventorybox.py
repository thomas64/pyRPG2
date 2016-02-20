
"""
class: InventoryBox
"""

import pygame

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

BOXWIDTH = 315
BOXHEIGHT = 670
TITLEX, TITLEY = 7, 1

TITLE = "Inventory"

FONTCOLOR = pygame.Color("white")
FONT = 'impact'
LARGEFONTSIZE = 25
NORMALFONTSIZE = 15


class InventoryBox(object):
    """
    Alle weergegeven informatie van alle inventory van de party.
    """
    def __init__(self, position):
        self.surface = pygame.Surface((BOXWIDTH, BOXHEIGHT))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.background = pygame.Surface(self.surface.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

    def _update(self, hero):
        self.title = self.largefont.render(TITLE, True, FONTCOLOR)

    def draw(self, screen, hero):
        """
        Update eerst de data, en teken dan al die data op de surface en die op de screen.
        :param screen: self.screen van partyscreen
        :param hero: de huidige geselecteerde hero
        """
        self._update(hero)

        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.background, LINECOLOR, self.surface.get_rect(), 1)

        self.surface.blit(self.title, (TITLEX, TITLEY))

        screen.blit(self.surface, self.rect.topleft)
