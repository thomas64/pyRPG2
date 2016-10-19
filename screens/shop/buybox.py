
"""
class: BuyBox
"""

import pygame

from constants import Keys
from inventoryitems import EquipmentItem

COLORKEY = pygame.Color("white")
LINECOLOR = pygame.Color("black")
SELECTCOLOR = pygame.Color("gray60")

FONTCOLOR = pygame.Color("black")
FONT = 'impact'
FONTSIZE = 15

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 285
COLUMNSY = 0
ROWHEIGHT = 34
ICONOFFSET = 1
TEXTOFFSET = 7
SUBSURW, SUBSURH = 32, 32

SCROLLSPEED = 17

TRANSP = 'resources/sprites/transp.png'


class BuyBox(object):
    """
    De box waar alle items uit de database te zien zijn, mits ze de 'shop' eigenschap hebben.
    """
    def __init__(self, x, y, width, height, equipment_database, sum_merchant):
        self.box_width = width
        self.box_height = height
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey(COLORKEY)
        self.surface = self.surface.convert()

        self.rect = self.surface.get_rect()
        self.rect.topleft = x, y

        self.sale = sum_merchant

        self.table_data = []
        self._fill_table_data(equipment_database)
        self.table_view = []
        self._setup_table_view()

        self.background = pygame.Surface((width, self.layer_height))
        self.background.fill(COLORKEY)
        self.background = self.background.convert()

        self.cur_item = None

        self._update_rects_in_layer_rect_with_offset()

    # noinspection PyUnresolvedReferences
    def _fill_table_data(self, equipment_database):

        for equipment_item in equipment_database.values():
            if equipment_item['shp']:
                equipment_item_obj = EquipmentItem(**equipment_item)
                equipment_item_spr = pygame.image.load(equipment_item_obj.SPR).subsurface(
                    equipment_item_obj.COL, equipment_item_obj.ROW, SUBSURW, SUBSURH).convert_alpha()
                equipment_item_nam = equipment_item_obj.NAM
                equipment_item_val = str(round(equipment_item_obj.VAL - ((equipment_item_obj.VAL / 100) * self.sale)))
                self.table_data.append(
                    # row[0],                   row[1],         row[2],         row[3],     row[4]
                    [equipment_item_spr, equipment_item_nam, equipment_item_val, None, equipment_item_obj]
                )

    def _setup_table_view(self):
        """
        Zet table_data om in een visuele weergave.
        """
        normalfont = pygame.font.SysFont(FONT, FONTSIZE)

        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(row[0])
            self.table_view[index].append(normalfont.render(row[1], True, FONTCOLOR).convert_alpha())
            self.table_view[index].append(normalfont.render(row[2], True, FONTCOLOR).convert_alpha())

        self.layer_height = COLUMNSY + len(self.table_view) * ROWHEIGHT
        if self.layer_height < self.box_height:
            self.layer_height = self.box_height
        self.layer = pygame.Surface((self.box_width, self.layer_height))
        self.layer = self.layer.convert()
        self.lay_rect = self.layer.get_rect()
        self.lay_rect.topleft = self.rect.topleft

    def _update_rects_in_layer_rect_with_offset(self):
        """
        Voeg de rects toe in row[3] van table_data waarmee gecorrespondeert kan worden met de muis bijvoorbeeld.
        Deze rects zijn variabel omdat er gescrollt kan worden, daarom wordt lay_rect voor de offset gebruikt.
        De offset is weer nodig omdat de rects in een box staat die weer een eigen positie op het scherm heeft.
        Na het scrollen wordt deze telkens weer geupdate.
        """
        for index, row in enumerate(self.table_data):
            row[3] = pygame.Rect(self.lay_rect.x + COLUMN1X, self.lay_rect.y + COLUMNSY + index * ROWHEIGHT,
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
            if self.lay_rect.y - self.rect.y > self.rect.height - self.layer_height + 2:  # zie sellbox voor de +2
                self.lay_rect.y -= SCROLLSPEED

        self._update_rects_in_layer_rect_with_offset()

    def mouse_hover(self, event):
        """
        Als de muis over een item uit row[3] van table_data gaat. Dat zijn de rects.
        Zet cur_item op de index van degene waar de muis over gaat.
        :param event: pygame.MOUSEMOTION uit shopscreen
        :return: row[4] is de kolom met het Object EquipmentItem.
        """
        for index, row in enumerate(self.table_data):
            if row[3].collidepoint(event.pos):
                self.cur_item = index
                return row[4].display()

    def mouse_click(self, event):
        """
        :param event: pygame.MOUSEBUTTONDOWN uit shopscreen
        """
        for index, row in enumerate(self.table_data):
            if row[3].collidepoint(event.pos):
                self.cur_item = index
                selected_item = row[4]
                value = int(row[2])

                return True, selected_item, value

        return False, None, None

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
