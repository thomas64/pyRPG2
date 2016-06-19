
"""
class: InfoBox
"""

import pygame

from components import TextBox

LINECOLOR = pygame.Color("black")
FONTCOLOR = pygame.Color("black")


class InfoBox(TextBox):
    """
    Waar in het shopscreen alle omschrijvingen worden weergegeven.
    """
    def __init__(self, x, y, width, height):
        super().__init__((x, y), width, height)

        self.fontcolor = FONTCOLOR
        self.linecolor = LINECOLOR
