
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

COLUMN1X = 0
COLUMN2X = 35
COLUMN3X = 285
COLUMNSY = 0
ROWHEIGHT = 35
ICONOFFSET = 2
TEXTOFFSET = 7


class OwnBox(object):
    """
    De box waarin de spells per persoon te zien zijn.
    Deze class bevat heel veel van sellbox uit shop.
    """
    def __init__(self, x, y, width, height, hero):
        self.box_width = width
        self.box_height = height
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey(COLORKEY)
        self.surface = self.surface.convert()

        self.rect = self.surface.get_rect()
        self.rect.topleft = x, y

        self.table_data = []
        self._fill_table_data(hero)
        self.table_view = []
        self._setup_table_view()

        self.background = pygame.Surface((width, self.layer_height))
        self.background.fill(COLORKEY)
        self.background = self.background.convert()

        self.cur_item = None

        self._update_rects_in_layer_rect_with_offset()

    def _fill_table_data(self, hero):

        for spell in hero.scl.get_all_spells():
            self.table_data.append(
                # row[0],       row[1],           row[2],        row[3],     row[4],    row[5], row[6], row[7]
                [spell.ICON, spell.NAM + " :", str(spell.qty), spell.DESC, spell.COL, spell.ROW, spell, None]
            )

    def _setup_table_view(self):
        """
        Zet table_data om in een visuele weergave.
        """
        normalfont = pygame.font.SysFont(FONT, FONTSIZE)

        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(pygame.image.load(row[0]).subsurface(row[4], row[5], 32, 32).convert_alpha())
            self.table_view[index].append(normalfont.render(row[1], True, FONTCOLOR).convert_alpha())
            self.table_view[index].append(normalfont.render(row[2], True, FONTCOLOR).convert_alpha())

        # stel de scroll layer in
        self.layer_height = COLUMNSY + len(self.table_view) * ROWHEIGHT
        if self.layer_height < self.box_height:
            self.layer_height = self.box_height
        self.layer = pygame.Surface((self.box_width, self.layer_height))
        self.layer = self.layer.convert()
        self.lay_rect = self.layer.get_rect()
        self.lay_rect.topleft = self.rect.topleft

    def _update_rects_in_layer_rect_with_offset(self):
        """
        Voeg de rects toe in row[7] van table_data waarmee gecorrespondeert kan worden met de muis bijvoorbeeld.
        Deze rects zijn variabel omdat er gescrollt kan worden, daarom wordt lay_rect voor de offset gebruikt.
        De offset is weer nodig omdat de rects in een box staat die weer een eigen positie op het scherm heeft.
        Na het scrollen wordt deze telkens weer geupdate.
        """
        for index, row in enumerate(self.table_data):
            row[7] = pygame.Rect(self.lay_rect.x + COLUMN1X, self.lay_rect.y + COLUMNSY + index * ROWHEIGHT,
                                 self.box_width, ROWHEIGHT+1)

    def mouse_hover(self, event):
        """
        Als de muis over een item uit row[7] van table_data gaat. Dat zijn de rects.
        Zet cur_item op de index van degene waar de muis over gaat.
        :param event: pygame.MOUSEMOTION uit shopscreen
        :return: row[6] is de kolom met het Object Spell.
        """
        for index, row in enumerate(self.table_data):
            if row[7].collidepoint(event.pos):
                self.cur_item = index
                return row[6].DESC

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
        pygame.draw.line(self.surface, LINECOLOR, (COLUMN2X, COLUMNSY), (COLUMN2X, self.layer_height))
        pygame.draw.line(self.surface, LINECOLOR, (COLUMN3X, COLUMNSY), (COLUMN3X, self.layer_height))

        # horizontale vierkanten
        for index, row in enumerate(range(0, int(self.layer_height / ROWHEIGHT))):
            if index == self.cur_item:
                pygame.draw.rect(self.layer, SELECTCOLOR,
                                 (COLUMN1X, COLUMNSY + index * ROWHEIGHT, self.box_width, ROWHEIGHT+1), 0)
            pygame.draw.rect(self.layer, LINECOLOR,
                             (COLUMN1X, COLUMNSY + index * ROWHEIGHT, self.box_width, ROWHEIGHT+1), 1)

        for index, row in enumerate(self.table_view):
            self.layer.blit(row[0], (COLUMN1X + ICONOFFSET, COLUMNSY + ICONOFFSET + index * ROWHEIGHT))
            self.layer.blit(row[1], (COLUMN2X + TEXTOFFSET, COLUMNSY + TEXTOFFSET + index * ROWHEIGHT))
            self.layer.blit(row[2], (COLUMN3X + TEXTOFFSET, COLUMNSY + TEXTOFFSET + index * ROWHEIGHT))

        screen.blit(self.surface, self.rect.topleft)
