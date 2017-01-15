
"""
class: InventoryBox
"""

import pygame

from components import ListBox
from constants import ColumnType

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 68
COLUMN4X = 102

TOTALCOLUMNS = ((ColumnType.f_icon, COLUMN1X, "", ""),
                (ColumnType.f_icon, COLUMN2X, "", ""),
                (ColumnType.text,   COLUMN3X, "Item", "Qty:"),
                (ColumnType.text,   COLUMN4X, "Item", "Name:"))


class InventoryBox(ListBox):
    """
    De box waar je gedeeltelijke inventory in te zien is.
    """
    def __init__(self, x, y, width, height, equipment_type, party, pouch, equipment):
        super().__init__(x, y, width, height)

        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X    # deze is voor de baseclass
        self.row_nr_with_rect = 5   # row[5]
        self.row_nr_with_obj = 4    # row[4]

        self.table_data = []
        self._fill_table_data(equipment_type, party, pouch, equipment)
        self.table_view = []
        self._setup_table_view()
        self._setup_scroll_layer()

        self.cur_item = None
        self._update_rects_in_layer_rect_with_offset()

    def _fill_table_data(self, equipment_type, party, pouch, equipment):

        black_spr = pygame.image.load(self.transp).convert_alpha()

        for resource_item in pouch.get_all_resource_items():
            resource_item_spr = pygame.image.load(resource_item.SPR).convert_alpha()
            self.table_data.append(
                # row[0],          row[1],              row[2],             row[3],          row[4],    row[5]
                [black_spr, resource_item_spr, str(resource_item.qty), resource_item.NAM, resource_item, None]
            )

        # hieronder volgt bijna een exacte kopie van sellbox.

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
                self.table_data.append(
                    # row[0],       row[1],       row[2],     row[3],          row[4]      row[5]
                    [hero_spr, equipment_item_spr, "1", equipment_item_nam, equipment_item, None]
                )

        # de rijen van equipment uit inventory.
        for equipment_item in equipment.get_all_equipment_items_of_type(equipment_type):
            equipment_item_spr = pygame.image.load(equipment_item.SPR).subsurface(
                equipment_item.COL, equipment_item.ROW, self.subsurw, self.subsurh).convert_alpha()
            if equipment_item.get_value_of('SKL'):
                equipment_item_nam = "[" + equipment_item.SKL.value + "] " + equipment_item.NAM
                if "Shield" in equipment_item_nam:
                    equipment_item_nam = equipment_item.NAM
            else:
                equipment_item_nam = equipment_item.NAM
            self.table_data.append(
                # row[0],        row[1],            row[2],                     row[3],         row[4],     row[5]
                [black_spr, equipment_item_spr, str(equipment_item.qty), equipment_item_nam, equipment_item, None]
            )
