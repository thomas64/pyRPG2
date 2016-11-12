
"""
class: SellBox
"""

import pygame

from components import ListBox
from constants import EquipmentType


COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 68
COLUMN4X = 102
COLUMN5X = 350

TOTALCOLUMNS = (('icon', COLUMN1X), ('icon', COLUMN2X), ('text', COLUMN3X), ('text', COLUMN4X), ('text', COLUMN5X))


class SellBox(ListBox):
    """
    De box waar je inventory in te zien is.
    """
    def __init__(self, x, y, width, height, equipment_type, party, inventory, sum_merchant):
        super().__init__(x, y, width, height)

        self.sale = sum_merchant

        self.table_data = []
        self._fill_table_data(equipment_type, party, inventory)
        self.table_view = []
        self._setup_table_view()
        self._setup_scroll_layer()

        self.background = pygame.Surface((width, self.layer_height))
        self.background.fill(self.colorkey)
        self.background = self.background.convert()

        self.cur_item = None

        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X    # deze is voor de baseclass
        self.row_nr_with_rect = 6   # row[6]
        self.row_nr_with_obj = 5    # row[5]
        self._update_rects_in_layer_rect_with_offset(self.row_nr_with_rect)

    def _fill_table_data(self, equipment_type, party, inventory):

        black_spr = pygame.image.load(self.transp).convert_alpha()

        if equipment_type == EquipmentType.itm:
            # inventory is hier pouch
            for pouch_item_obj in inventory.get_all_pouch_items():
                # party is hier shopdatabase
                for pouch_item_dict in party.values():
                    if pouch_item_obj.NAM == pouch_item_dict['nam']:
                        pouch_item_spr = pygame.image.load(pouch_item_obj.SPR).convert_alpha()
                        pouch_item_nam = pouch_item_obj.NAM
                        pouch_item_val = str(round(pouch_item_obj.VAL / 2 + ((pouch_item_obj.VAL / 200) * self.sale)))
                        self.table_data.append(
                            # row[0],       row[1],         row[2],             row[3],             row[4]
                            [black_spr, pouch_item_spr, str(pouch_item_obj.qty), pouch_item_nam, pouch_item_val,
                             # row[5],      row[6], [7]
                             pouch_item_obj, None,  ""]
                        )
                        break

        else:
            # hieronder volgt bijna een exacte kopie van invclickbox

            # de rijen van equipment van hero's
            for hero in party.values():  # in invclickbox staat er geen values() omdat party dan een list is.
                # haal de equipment item op uit het type
                equipment_item = hero.get_equipped_item_of_type(equipment_type)
                # "if equipment_item" is voor sellbox, bijv bij sword dan geeft iemand met een pole None terug en
                # dan werkt .is_not_empty() niet.
                if equipment_item and equipment_item.is_not_empty():
                    # laad de hero subsprite
                    hero_spr = pygame.image.load(hero.SPR).subsurface(32, 0, self.subsurw, self.subsurh).convert_alpha()
                    # laad de item subsprite
                    equipment_item_spr = pygame.image.load(equipment_item.SPR).subsurface(
                        equipment_item.COL, equipment_item.ROW, self.subsurw, self.subsurh).convert_alpha()
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
                    equipment_item.COL, equipment_item.ROW, self.subsurw, self.subsurh).convert_alpha()
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

    def _setup_table_view(self):
        """
        Zet table_data om in een visuele weergave.
        """
        normalfont = pygame.font.SysFont(self.font, self.fontsize)

        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(row[0])
            self.table_view[index].append(row[1])
            self.table_view[index].append(normalfont.render(row[2], True, self.fontcolor).convert_alpha())
            self.table_view[index].append(normalfont.render(row[3], True, self.fontcolor).convert_alpha())
            self.table_view[index].append(normalfont.render(row[4], True, self.fontcolor).convert_alpha())

    def mouse_click(self, event):
        """
        :param event: pygame.MOUSEBUTTONDOWN uit shopscreen
        """
        for index, row in enumerate(self.table_data):
            if row[6].collidepoint(event.pos):
                self.cur_item = index
                selected_item = row[5]
                quantity = int(row[2])
                value = int(row[4])

                if row[7] != "X":       # verschil tussen heroes en equipment/pouch
                    return True, selected_item, quantity, value
                else:
                    return True, None,          None,     None

        return False,            None,          None,     None
