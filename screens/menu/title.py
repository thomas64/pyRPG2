
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


class Title(object):
    """
    De mainmenu titel.
    """
    def __init__(self):
        self.titlefont = pygame.font.SysFont(TITLEFONT, TITLEFONTSIZE)
        self.subfont = pygame.font.SysFont(SUBFONT, SUBFONTSIZE)
        self.title = self.titlefont.render(TITLETEXT, True, TITLEFONTCOLOR)
        self.sub = self.subfont.render(SUBTEXT, True, SUBFONTCOLOR)

    def draw(self, screen):
        """
        Tekent de titel op de screen.
        :param screen: self.screen van de menuscreen
        """
        screen.blit(self.title, (TITLEPOSX, TITLEPOSY))
        screen.blit(self.sub, (SUBPOSX, SUBPOSY))
