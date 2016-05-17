
"""
class: SellBox
"""

import pygame

import keys

COLORKEY = pygame.Color("white")
LINECOLOR = pygame.Color("black")
SELECTCOLOR = pygame.Color("gray60")

FONTCOLOR = pygame.Color("black")
FONT = 'impact'
LARGEFONTSIZE = 25
NORMALFONTSIZE = 15

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 68
COLUMN4X = 102
COLUMN5X = 285
COLUMNSY = 0
ROWHEIGHT = 34
ICONOFFSET = 1
TEXTOFFSET = 7
SUBSURW, SUBSURH = 32, 32

SCROLLSPEED = 17

TRANSP = 'resources/sprites/transp.png'


class SellBox(object):
    """
    ...
    """
    def __init__(self, x, y, width, height, equipment_type, party, inventory):
        self.box_width = width
        self.box_height = height
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey(COLORKEY)
        self.surface = self.surface.convert()

        self.rect = self.surface.get_rect()
        self.rect.topleft = x, y

        largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)

        self.sale = party.get_sum_value_of_skill("mer")

        self.table_data = list()
        self._fill_table_data(equipment_type, party, inventory)

        self.table_view = []
        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(row[0])
            self.table_view[index].append(row[1])
            self.table_view[index].append(normalfont.render(row[2], True, FONTCOLOR).convert_alpha())
            self.table_view[index].append(normalfont.render(row[3], True, FONTCOLOR).convert_alpha())
            self.table_view[index].append(normalfont.render(row[4], True, FONTCOLOR).convert_alpha())

        # stel de scroll layer in
        self.layer_height = COLUMNSY + len(self.table_view) * ROWHEIGHT
        if self.layer_height < height:
            self.layer_height = height
        self.layer = pygame.Surface((width, self.layer_height))
        self.layer = self.layer.convert()
        self.lay_rect = self.layer.get_rect()
        self.lay_rect.topleft = x, y

        self.background = pygame.Surface((width, self.layer_height))
        self.background.fill(COLORKEY)
        self.background = self.background.convert()

        self.cur_item = None

        self._update_rects_in_layer_rect_with_offset()

    def _fill_table_data(self, equipment_type, party, inventory):
        # hieronder volgt bijna een exacte kopie van invclickbox

        black_spr = pygame.image.load(TRANSP).convert_alpha()

        # de rijen van equipment van hero's
        for hero in list(party.values()):
            # haal de equipment item op uit het type
            equipment_item = hero.get_equipped_item_of_type(equipment_type)
            if equipment_item.is_not_empty():
                # laad de hero subsprite
                hero_spr = pygame.image.load(hero.SPR).subsurface(32, 0, SUBSURW, SUBSURW).convert_alpha()
                # laad de item subsprite
                equipment_item_spr = pygame.image.load(equipment_item.SPR).subsurface(
                    equipment_item.COL, equipment_item.ROW, SUBSURW, SUBSURH).convert_alpha()
                # als een equipment item een skill waarde heeft, zoals eigenlijk alleen bij wapens
                if equipment_item.get_value_of('SKL'):
                    # zet dat dan voor de naam
                    equipment_item_nam = "[" + equipment_item.SKL.value + "] " + equipment_item.NAM
                    # maar bij een schild niet, want die heeft ook een skill waarde, maar niet om zichtbaar te maken
                    if "Shield" in equipment_item_nam:
                        equipment_item_nam = equipment_item.NAM
                else:
                    # en anders gewoon de naam
                    equipment_item_nam = equipment_item.NAM
                equipment_item_val = str(round(equipment_item.VAL / 2 + ((equipment_item.VAL / 200) * self.sale)))
                self.table_data.append(
                    # row[0],       row[1],       row[2],     row[3],             row[4]
                    [hero_spr, equipment_item_spr, "1", equipment_item_nam, equipment_item_val,
                        # row[5],   row[6], [7]
                     equipment_item, None, "X"]
                )

        # de rijen van equipment uit inventory.
        for equipment_item in inventory.get_all_equipment_items_of_type(equipment_type):
            equipment_item_spr = pygame.image.load(equipment_item.SPR).subsurface(
                equipment_item.COL, equipment_item.ROW, SUBSURW, SUBSURH).convert_alpha()
            if equipment_item.get_value_of('SKL'):
                equipment_item_nam = "[" + equipment_item.SKL.value + "] " + equipment_item.NAM
                if "Shield" in equipment_item_nam:
                    equipment_item_nam = equipment_item.NAM
            else:
                equipment_item_nam = equipment_item.NAM
            equipment_item_val = str(round(equipment_item.VAL / 2 + ((equipment_item.VAL / 200) * self.sale)))
            self.table_data.append(
                # row[0],        row[1],            row[2],                     row[3],           row[4]
                [black_spr, equipment_item_spr, str(equipment_item.qty), equipment_item_nam, equipment_item_val,
                    # row[5],   row[6], [7]
                 equipment_item, None, ""]
            )

    def _update_rects_in_layer_rect_with_offset(self):
        """
        Voeg de rects toe in row[6] van table_data waarmee gecorrespondeert kan worden met de muis bijvoorbeeld.
        Deze rects zijn variabel omdat er gescrollt kan worden, daarom wordt lay_rect voor de offset gebruikt.
        De offset is weer nodig omdat de rects in een box staat die weer een eigen positie op het scherm heeft.
        Na het scrollen wordt deze telkens weer geupdate.
        """
        for index, row in enumerate(self.table_data):
            row[6] = pygame.Rect(self.lay_rect.x + COLUMN1X, self.lay_rect.y + COLUMNSY + index * ROWHEIGHT,
                                 self.box_width, ROWHEIGHT+1)

    def mouse_scroll(self, event):
        """
        Registreert of scrolwiel gebruikt wordt. Verplaatst de layer dan omhoog of omlaag.
        :param event: pygame.MOUSEBUTTONDOWN uit shopscreen
        """
        if event.button == keys.SCROLLUP:
            if self.lay_rect.y - self.rect.y < 0:
                self.lay_rect.y += SCROLLSPEED
        elif event.button == keys.SCROLLDOWN:
            if self.lay_rect.y - self.rect.y > self.rect.height - self.layer_height:
                self.lay_rect.y -= SCROLLSPEED

        self._update_rects_in_layer_rect_with_offset()

    def mouse_hover(self, event):
        """
        Als de muis over een item uit row[6] van table_data gaat. Dat zijn de rects.
        Zet cur_item op de index van degene waar de muis over gaat.
        :param event: pygame.MOUSEMOTION uit shopscreen
        :return: row[5] is de kolom met het Object EquipmentItem.
        """
        for index, row in enumerate(self.table_data):
            if row[6].collidepoint(event.pos):
                self.cur_item = index
                # dit hieronder is nog uit invclickbox, hier moet ik later nog wat mee
                # equipment_item = row[5]
                # if equipment_item.is_not_empty():
                #     return equipment_item.display(), equipment_item
                # return None, equipment_item

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
        pygame.draw.line(self.surface, LINECOLOR, (COLUMN4X, COLUMNSY), (COLUMN4X, self.layer_height))
        pygame.draw.line(self.surface, LINECOLOR, (COLUMN5X, COLUMNSY), (COLUMN5X, self.layer_height))

        # horizontale vierkanten
        for index, row in enumerate(range(0, int(self.layer_height / ROWHEIGHT))):
            if index == self.cur_item:
                pygame.draw.rect(self.layer, SELECTCOLOR,
                                 (COLUMN1X, COLUMNSY + index * ROWHEIGHT, self.box_width, ROWHEIGHT+1), 0)
            pygame.draw.rect(self.layer, LINECOLOR,
                             (COLUMN1X, COLUMNSY + index * ROWHEIGHT, self.box_width, ROWHEIGHT+1), 1)

        for index, row in enumerate(self.table_view):
            self.layer.blit(row[0], (COLUMN1X + ICONOFFSET, COLUMNSY + ICONOFFSET + index * ROWHEIGHT))
            self.layer.blit(row[1], (COLUMN2X + ICONOFFSET, COLUMNSY + ICONOFFSET + index * ROWHEIGHT))
            self.layer.blit(row[2], (COLUMN3X + TEXTOFFSET, COLUMNSY + TEXTOFFSET + index * ROWHEIGHT))
            self.layer.blit(row[3], (COLUMN4X + TEXTOFFSET, COLUMNSY + TEXTOFFSET + index * ROWHEIGHT))
            self.layer.blit(row[4], (COLUMN5X + TEXTOFFSET, COLUMNSY + TEXTOFFSET + index * ROWHEIGHT))

        screen.blit(self.surface, self.rect.topleft)
