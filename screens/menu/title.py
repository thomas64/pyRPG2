
"""
class: MenuTitle
"""

import pygame

TITLETEXT = "pyRPG"
TITLEFONT = 'colonna'
TITLEFONTSIZE = 100
TITLEFONTCOLOR = pygame.Color("black")
TITLEPOSX = 150
TITLEPOSY = 50

SUBTEXT = "THE LOST GATE"
SUBFONT = None
SUBFONTSIZE = 50
SUBFONTCOLOR = pygame.Color("gray36")
SUBPOSX = 155
SUBPOSY = 160

VERSIONTEXT = "PreAlpha v0.005"
VERSIONFONT = 'verdana'
VERSIONFONTSIZE = 12
VERSIONFONTCOLOR = pygame.Color("black")
VERSIONPOSX = -120
VERSIONPOSY = -20


class Title(object):
    """
    De mainmenu titel.
    """
    def __init__(self):
        self.titlefont = pygame.font.SysFont(TITLEFONT, TITLEFONTSIZE)
        self.subfont = pygame.font.SysFont(SUBFONT, SUBFONTSIZE)
        self.versionfont = pygame.font.SysFont(VERSIONFONT, VERSIONFONTSIZE)
        self.title = self.titlefont.render(TITLETEXT, True, TITLEFONTCOLOR).convert_alpha()
        self.sub = self.subfont.render(SUBTEXT, True, SUBFONTCOLOR).convert_alpha()
        self.version = self.versionfont.render(VERSIONTEXT, True, VERSIONFONTCOLOR).convert_alpha()

    def render(self, screen):
        """
        Tekent de titel op de screen.
        :param screen: self.screen van de menuscreen
        """
        screen.blit(self.title, (TITLEPOSX, TITLEPOSY))
        screen.blit(self.sub, (SUBPOSX, SUBPOSY))
        screen.blit(self.version, (screen.get_width() + VERSIONPOSX, screen.get_height() + VERSIONPOSY))
