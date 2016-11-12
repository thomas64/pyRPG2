
"""
class: PouchBox
"""

import pygame

from .basebox import BaseBox


LINECOLOR = pygame.Color("white")

TITLEX, TITLEY = 7, 1
COLUMN1X = 50
COLUMN2X = 90
COLUMN3X = 240
COLUMNSY = 50
ROWHEIGHT = 30
ICONOFFSET = -6

TITLE = "Pouch"


class PouchBox(BaseBox):
    """
    Alle weergegeven informatie van alle pouchitems van de party.
    """
    def __init__(self, position, width, height):
        super().__init__(position, width, height)

        self.title = self.largefont.render(TITLE, True, self.fontcolor1).convert_alpha()

    def update(self, pouch):
        """
        Update eerst alle data.
        :param pouch:
        """
        self.table_data = []
        for pouch_item in pouch.get_all_pouch_items():
            self.table_data.append(
                # row[0],           row[1],                 row[2],         row[3],    row[4
                [pouch_item.SPR, pouch_item.NAM + " :", str(pouch_item.qty), None, pouch_item.DESC]
            )

        for index, row in enumerate(self.table_data):
            row[3] = self._create_rect_with_offset(index, row[1], COLUMN2X, COLUMNSY, ROWHEIGHT)

        self.table_view = []
        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(pygame.image.load(row[0]).convert_alpha())
            self.table_view[index].append(self.normalfont.render(row[1], True, self._get_color(index)).convert_alpha())
            self.table_view[index].append(self.normalfont.render(row[2], True, self.fontcolor1).convert_alpha())

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
