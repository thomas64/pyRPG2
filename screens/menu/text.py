
"""
class: MenuText
"""

import pygame


class Text(object):
    """
    Een mainmenu item.
    """
    def __init__(self, item, index, font, size, color):
        self.func = item[0]     # de eerste van de double tuple, bijv NewGame
        self.text = item[1]     # de tweede van de double tuple, bijv New Game
        self.index = index
        self.font = pygame.font.SysFont(font, size)
        self.font_color = color
        self.label = self.font.render(self.text, True, self.font_color)
        self.rect = self.label.get_rect()
        self.width = self.label.get_width()
        self.height = self.label.get_height()
        self.position = (0, 0)

    def set_font_color(self, color):
        """
        Geef een menu item een bepaalde kleur.
        :param color: pygame.Color("kleurnaam")
        """
        self.font_color = color
        self.label = self.font.render(self.text, True, self.font_color)
