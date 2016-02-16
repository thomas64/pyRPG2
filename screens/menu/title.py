
"""
class: MenuTitle
"""

import pygame

TITLETEXT = "pyRPG"
TITLEFONT = 'colonna'
TITLEFONTSIZE = 150
TITLEFONTCOLOR = pygame.Color("red")
TITLEPOSY = 125


class Title(object):
    """
    De mainmenu titel.
    """
    def __init__(self):
        self.text = TITLETEXT
        self.font = pygame.font.SysFont(TITLEFONT, TITLEFONTSIZE)
        self.font_color = TITLEFONTCOLOR
        self.label = self.font.render(self.text, True, self.font_color)
        self.width = self.label.get_width()
        self.height = self.label.get_height()
        self.position = (0, 0)

    def set_position(self, screen_width):
        """
        Zet de titel op de juiste positie.
        :param screen_width: de totale breedte van de achtergrond waarop de title zich bevind.
        """
        pos_x = (screen_width/2) - (self.width/2)
        pos_y = TITLEPOSY
        self.position = (pos_x, pos_y)
