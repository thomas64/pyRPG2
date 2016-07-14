
"""
class: MenuText
"""

import pygame

MENUFONT = None             # todo, nog een ander font kiezen?
MENUFONTSIZE = 50


class MenuText(object):
    """
    Een mainmenu item.
    """
    def __init__(self, menu_string, index, color):
        self.text = menu_string  # bijv 'New Game'.
        self.index = index       # index is voor mousemotion in display.
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

    def set_position(self, pos_x, pos_y):
        """
        Stelt de positie in van het text item.
        :param pos_x: de x positie
        :param pos_y: de y positie
        """
        self.position = (pos_x, pos_y)
        self.rect.topleft = self.position

    def flip_switch(self):
        """
        Wanneer aangeroepen verandert deze de visuele weergave van de tekst.
        """
        if "Off" in self.text:
            self.text = self.text.replace("Off", "On")
        elif "On" in self.text:
            self.text = self.text.replace("On", "Off")

    def clear_save_slot(self, screen, index):
        """
        Wanneer op delete gedrukt in het load of save menu, reset dan de tekst naar '...'
        :param screen: het scherm
        :param index: visusele weergave van de hoeveelste slot, het is dus eigenlijk index+1
        """
        # pas de tekst aan
        self.text = "Slot {}:  ...".format(index)
        # render de tekst in het label, zodat hij de grootte weet
        self.label = self.font.render(self.text, True, self.font_color).convert_alpha()
        # herbereken x
        pos_x = (screen.get_width() - self.label.get_width()) / 2
        # gebruik de oude y
        pos_y = self.rect.y
        # zet de nieuwe positie
        self.set_position(pos_x, pos_y)
