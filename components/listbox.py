
"""
class: ListBox
"""

import pygame

from console import Console
from constants import Keys


COLORKEY = pygame.Color("white")
LINECOLOR = pygame.Color("black")
SELECTCOLOR = pygame.Color("gray60")

FONTCOLOR = pygame.Color("black")
FONT = 'impact'
FONTSIZE = 15

COLUMNSY = 0
ROWHEIGHT = 34
ICONOFFSET = 1
TEXTOFFSET = 7
SUBSURW, SUBSURH = 32, 32

SCROLLSPEED = 17

TRANSP = 'resources/sprites/transp.png'


class ListBox(object):
    """
    Base class voor lijsten in shops bijv.
    """
    def __init__(self, x, y, width, height):
        self.box_width = width
        self.box_height = height
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey(COLORKEY)
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = x, y

        self.colorkey = COLORKEY
        self.linecolor = LINECOLOR
        self.selectcolor = SELECTCOLOR
        self.fontcolor = FONTCOLOR
        self.font = FONT
        self.fontsize = FONTSIZE
        self.columnsy = COLUMNSY
        self.rowheight = ROWHEIGHT
        self.iconoffset = ICONOFFSET
        self.textoffset = TEXTOFFSET
        self.subsurw = SUBSURW
        self.subsurh = SUBSURH
        self.scrollspeed = SCROLLSPEED
        self.transp = TRANSP

        self.cur_item = None

        self.background = None
        self.table_data = []
        self.table_view = []
        self.total_columns = []
        self.column1x = None
        self.layer = None
        self.lay_rect = None
        self.layer_height = None
        self.row_nr_with_rect = None
        self.row_nr_with_obj = None

    def _setup_scroll_layer(self):
        # stel de scroll layer in
        self.layer_height = self.columnsy + len(self.table_view) * self.rowheight
        if self.layer_height < self.box_height:
            self.layer_height = self.box_height
        self.layer = pygame.Surface((self.box_width, self.layer_height))
        self.layer = self.layer.convert()
        self.lay_rect = self.layer.get_rect()
        self.lay_rect.topleft = self.rect.topleft

    def _update_rects_in_layer_rect_with_offset(self, row_nr):
        """
        Voeg de rects toe in row[6] van table_data waarmee gecorrespondeert kan worden met de muis bijvoorbeeld.
        Deze rects zijn variabel omdat er gescrollt kan worden, daarom wordt lay_rect voor de offset gebruikt.
        De offset is weer nodig omdat de rects in een box staat die weer een eigen positie op het scherm heeft.
        Na het scrollen wordt deze telkens weer geupdate.
        """
        for index, row in enumerate(self.table_data):
            row[row_nr] = pygame.Rect(self.lay_rect.x + self.column1x, self.lay_rect.y + COLUMNSY + index * ROWHEIGHT,
                                      self.box_width, ROWHEIGHT+1)

    def mouse_scroll(self, event):
        """
        Registreert of scrolwiel gebruikt wordt. Verplaatst de layer dan omhoog of omlaag.
        :param event: pygame.MOUSEBUTTONDOWN uit shopscreen
        """
        if event.button == Keys.Scrollup.value:
            if self.lay_rect.y - self.rect.y < 0:
                self.lay_rect.y += SCROLLSPEED
        elif event.button == Keys.Scrolldown.value:
            if self.lay_rect.y - self.rect.y > self.rect.height - self.layer_height + 2:  # +2 is nodig tegen scroll-
                self.lay_rect.y -= SCROLLSPEED                                            # ghosting bij hoogte 1/4

        self._update_rects_in_layer_rect_with_offset(self.row_nr_with_rect)

    def mouse_hover(self, event):
        """
        Als de muis over een item uit row[row_with_rect] van table_data gaat. Dat zijn de rects.
        Zet cur_item op de index van degene waar de muis over gaat.
        :param event: pygame.MOUSEMOTION uit shopscreen
        :return: row[row_with_obj] is de kolom met het Object EquipmentItem/Spell/etc.
        """
        for index, row in enumerate(self.table_data):
            if row[self.row_nr_with_rect].collidepoint(event.pos):
                self.cur_item = index
                return row[self.row_nr_with_obj].show_info()

    def render(self, screen):
        """
        Surface tekent layer, de rest gaat op de layer, en screen tekent de surface.
        :param screen: self.screen van shopscreen
        """
        self.surface.blit(self.layer, (0, self.lay_rect.y - self.rect.y))
        self.layer.blit(self.background, (0, 0))

        # omranding
        pygame.draw.rect(self.surface, self.linecolor, self.surface.get_rect(), 1)
        # verticale lijnen
        for columnx in self.total_columns:
            pygame.draw.line(self.surface, self.linecolor, (columnx[1], self.columnsy), (columnx[1], self.layer_height))

        # horizontale vierkanten
        for index, row in enumerate(range(0, int(self.layer_height / self.rowheight))):
            if index == self.cur_item:
                pygame.draw.rect(self.layer, self.selectcolor,
                                 (self.column1x, self.columnsy + index * self.rowheight,
                                  self.box_width, self.rowheight + 1), 0)
            pygame.draw.rect(self.layer, self.linecolor,
                             (self.column1x, self.columnsy + index * self.rowheight,
                              self.box_width, self.rowheight + 1), 1)

        for index, row in enumerate(self.table_view):
            for row_nr, columnx in enumerate(self.total_columns):
                if columnx[0] == 'icon':
                    self.layer.blit(
                        row[row_nr],
                        (columnx[1] + self.iconoffset, self.columnsy + self.iconoffset + index * self.rowheight))
                elif columnx[0] == 'text':
                    self.layer.blit(
                        row[row_nr],
                        (columnx[1] + self.textoffset, self.columnsy + self.textoffset + index * self.rowheight))
                else:
                    Console.error_unknown_column_key()
                    raise KeyError

        screen.blit(self.surface, self.rect.topleft)
