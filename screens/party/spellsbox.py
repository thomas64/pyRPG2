
"""
class: SpellsBox
"""

import pygame

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

BOXWIDTH = 329
BOXHEIGHT = 640
TITLEX, TITLEY = 7, 1

TITLE = "Spells"

FONTCOLOR1 = pygame.Color("white")
FONTCOLOR2 = pygame.Color("yellow")
FONT = 'impact'
LARGEFONTSIZE = 25
NORMALFONTSIZE = 15


class SpellsBox(object):
    """
    Alle weergegeven informatie van alle spells van een hero.
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

        self.title = self.largefont.render(TITLE, True, FONTCOLOR1).convert_alpha()

    def update(self, hero):
        """
        Update eerst alle data.
        :param hero: de huidige geselecteerde hero uit partyscreen
        """

        pass

    def render(self, screen):
        """
        En teken dan al die data op de surface en die op de screen.
        :param screen: self.screen van partyscreen
        """
        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.background, LINECOLOR, self.surface.get_rect(), 1)

        self.surface.blit(self.title, (TITLEX, TITLEY))

        screen.blit(self.surface, self.rect.topleft)
