
"""
class: PouchBox
"""

import pygame

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

BOXWIDTH = 329
BOXHEIGHT = 290
TITLEX, TITLEY = 7, 1
COLUMN1X = 50
COLUMN2X = 90
COLUMN3X = 190
COLUMNSY = 60
ROWHEIGHT = 30
ICONOFFSET = -6

TITLE = "Pouch"

FONTCOLOR1 = pygame.Color("white")
FONTCOLOR2 = pygame.Color("yellow")
FONT = 'impact'
LARGEFONTSIZE = 25
NORMALFONTSIZE = 15


class PouchBox(object):
    """
    Alle weergegeven informatie van alle pouchitems van de party.
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

        self.cur_item = None

        self.title = self.largefont.render(TITLE, True, FONTCOLOR1).convert_alpha()
        self.table_data = []
        self.table_view = []

    def update(self, pouch):
        """
        Update eerst alle data.
        :param pouch:
        """
        self.table_data = []
        for pouch_item in sorted(pouch.values(), key=lambda xx: xx.SRT):
            self.table_data.append(
                # row[0],           row[1],                 row[2],         row[3]
                [pouch_item.SPR, pouch_item.NAM + " :", str(pouch_item.qty), None]
            )

        for index, row in enumerate(self.table_data):
            row[3] = self._create_rect_with_offset(index, row[1])

        self.table_view = []
        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(pygame.image.load(row[0]).convert_alpha())
            if index == self.cur_item:      # als de index van deze rij gelijk is aan waar de muis over zit,
                color = FONTCOLOR2          # maak hem geel
            else:                           # anders gewoon wit.
                color = FONTCOLOR1
            self.table_view[index].append(self.normalfont.render(row[1], True, color).convert_alpha())
            self.table_view[index].append(self.normalfont.render(row[2], True, FONTCOLOR1).convert_alpha())

    def render(self, screen):
        """
        En teken dan al die data op de surface en die op de screen.
        :param screen: self.screen van partyscreen
        """
        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.background, LINECOLOR, self.surface.get_rect(), 1)

        self.surface.blit(self.title, (TITLEX, TITLEY))
        for index, row in enumerate(self.table_view):
            self.surface.blit(row[0], (COLUMN1X, COLUMNSY + ICONOFFSET + index * ROWHEIGHT))
            self.surface.blit(row[1], (COLUMN2X, COLUMNSY + index * ROWHEIGHT))
            self.surface.blit(row[2], (COLUMN3X, COLUMNSY + index * ROWHEIGHT))

        screen.blit(self.surface, self.rect.topleft)

    def _create_rect_with_offset(self, index, text):
        """
        self.rect is de hele box zelf. Die heeft ook een position op het scherm, vandaar dat de position een soort
        offset moet krijgen hier.
        """
        rect = self.normalfont.render(text, True, FONTCOLOR1).get_rect()
        rect.topleft = self.rect.left + COLUMN2X, (self.rect.top + COLUMNSY) + index * ROWHEIGHT
        return rect
