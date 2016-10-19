
"""
class: OwnBox
"""

import pygame

COLORKEY = pygame.Color("white")
LINECOLOR = pygame.Color("black")
SELECTCOLOR = pygame.Color("gray60")

FONTCOLOR = pygame.Color("black")
FONT = 'impact'
FONTSIZE = 15

COLUMNSY = 0
ROWHEIGHT = 34


class OwnBox(object):
    """
    De box waarin de spells per persoon te zien zijn.
    """
    def __init__(self, x, y, width, height):
        self.box_width = width
        self.box_height = height
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey(COLORKEY)
        self.surface = self.surface.convert()

        self.rect = self.surface.get_rect()
        self.rect.topleft = x, y

        self.table_data = []
        # self._fill_table_data(equipment_type, party, inventory)
        self.table_view = []
        self._setup_table_view()

        self.background = pygame.Surface((width, self.layer_height))
        self.background.fill(COLORKEY)
        self.background = self.background.convert()

    def _setup_table_view(self):
        """
        Zet table_data om in een visuele weergave.
        """
        normalfont = pygame.font.SysFont(FONT, FONTSIZE)

        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(row[0])
            self.table_view[index].append(row[1])
            self.table_view[index].append(normalfont.render(row[2], True, FONTCOLOR).convert_alpha())
            self.table_view[index].append(normalfont.render(row[3], True, FONTCOLOR).convert_alpha())
            self.table_view[index].append(normalfont.render(row[4], True, FONTCOLOR).convert_alpha())

        # stel de scroll layer in
        self.layer_height = COLUMNSY + len(self.table_view) * ROWHEIGHT
        if self.layer_height < self.box_height:
            self.layer_height = self.box_height
        self.layer = pygame.Surface((self.box_width, self.layer_height))
        self.layer = self.layer.convert()
        self.lay_rect = self.layer.get_rect()
        self.lay_rect.topleft = self.rect.topleft

    def render(self, screen):
        """
        Surface tekent layer, de rest gaat op de layer, en screen tekent de surface.
        :param screen: self.screen van shopscreen
        """
        self.surface.blit(self.layer, (0, self.lay_rect.y - self.rect.y))
        self.layer.blit(self.background, (0, 0))
        # omranding
        pygame.draw.rect(self.surface, LINECOLOR, self.surface.get_rect(), 1)
        # verticale lijnen
        # pygame.draw.line(self.surface, LINECOLOR, (COLUMN2X, COLUMNSY), (COLUMN2X, self.layer_height))
        # pygame.draw.line(self.surface, LINECOLOR, (COLUMN3X, COLUMNSY), (COLUMN3X, self.layer_height))
        # pygame.draw.line(self.surface, LINECOLOR, (COLUMN4X, COLUMNSY), (COLUMN4X, self.layer_height))
        # pygame.draw.line(self.surface, LINECOLOR, (COLUMN5X, COLUMNSY), (COLUMN5X, self.layer_height))

        # horizontale vierkanten
        # for index, row in enumerate(range(0, int(self.layer_height / ROWHEIGHT))):
        #     if index == self.cur_item:
        #         pygame.draw.rect(self.layer, SELECTCOLOR,
        #                          (COLUMN1X, COLUMNSY + index * ROWHEIGHT, self.box_width, ROWHEIGHT+1), 0)
        #     pygame.draw.rect(self.layer, LINECOLOR,
        #                      (COLUMN1X, COLUMNSY + index * ROWHEIGHT, self.box_width, ROWHEIGHT+1), 1)
        #
        # for index, row in enumerate(self.table_view):
        #     self.layer.blit(row[0], (COLUMN1X + ICONOFFSET, COLUMNSY + ICONOFFSET + index * ROWHEIGHT))
        #     self.layer.blit(row[1], (COLUMN2X + ICONOFFSET, COLUMNSY + ICONOFFSET + index * ROWHEIGHT))
        #     self.layer.blit(row[2], (COLUMN3X + TEXTOFFSET, COLUMNSY + TEXTOFFSET + index * ROWHEIGHT))
        #     self.layer.blit(row[3], (COLUMN4X + TEXTOFFSET, COLUMNSY + TEXTOFFSET + index * ROWHEIGHT))
        #     self.layer.blit(row[4], (COLUMN5X + TEXTOFFSET, COLUMNSY + TEXTOFFSET + index * ROWHEIGHT))

        screen.blit(self.surface, self.rect.topleft)
