
"""
class: InfoBox
"""

import pygame

BACKGROUNDCOLOR = pygame.Color("black")

FONTCOLOR = pygame.Color("white")
FONT = 'arial'
FONTSIZE = 14
LINEHEIGHT = 20


class InfoBox(object):
    """
    Waar in het partyscreen alle omschrijvingen worden weergegeven.
    """
    def __init__(self, position):
        self.surface = pygame.Surface((405, 160))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = position

        self.background = pygame.Surface(self.surface.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()

        self.font = pygame.font.SysFont(FONT, FONTSIZE)

    def draw(self, screen, text):
        """
        Teken het label bovenop de achtergrond.
        :param screen: self.screen van partyscreen
        :param text: de tekst om weer te geven
        """
        self.surface.blit(self.background, (0, 0))
        if type(text) == tuple:
            for i, line in enumerate(text):
                label = self.font.render(line, True, FONTCOLOR)
                self.surface.blit(label, (10, 10 + i * LINEHEIGHT))
        elif type(text) == str:
            label = self.font.render(text, True, FONTCOLOR)
            self.surface.blit(label, (10, 10))
        screen.blit(self.surface, self.rect.topleft)
