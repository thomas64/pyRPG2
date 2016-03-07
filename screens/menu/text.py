
"""
class: MenuText
"""

import pygame

MENUFONT = None             # todo, nog een ander font kiezen?
MENUFONTSIZE = 50


class Text(object):
    """
    Een mainmenu item.
    """
    def __init__(self, item, index, color):
        self.func = item[0]     # de eerste van de double tuple, bijv NewGame. dit is de key uit content
        self.text = item[1]     # de tweede van de double tuple, bijv New Game. dit is de value uit content
        self.index = index      # index is voor mousemotion in display.
        self.font = pygame.font.SysFont(MENUFONT, MENUFONTSIZE)
        self.font_color = color
        self.label = self.font.render(self.text, True, self.font_color).convert_alpha()
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
        self.label = self.font.render(self.text, True, self.font_color).convert_alpha()

    def flip_switch(self):
        """
        Wanneer aangeroepen verandert deze de visuele weergave van de tekst.
        """
        if "Off" in self.text:
            self.text = self.text.replace("Off", "On")
        elif "On" in self.text:
            self.text = self.text.replace("On", "Off")
