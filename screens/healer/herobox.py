
"""
class: HeroBox
"""

import pygame

from components import ListBox
from constants import ColumnType

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 134

TOTALCOLUMNS = ((ColumnType.f_icon, COLUMN1X, "", ""),
                (ColumnType.text,   COLUMN2X, "", ""),
                (ColumnType.text,   COLUMN3X, "", ""))


class HeroBox(ListBox):
    """
    De box waar je gedeeltelijke party in te zien is.
    """
    def __init__(self, x, y, width, height, party, healer):
        super().__init__(x, y, width, height)

        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X    # deze is voor de baseclass
        self.row_nr_with_rect = 4   # row[4]
        self.row_nr_with_obj = 3    # row[3]

        self.table_data = []
        self._fill_table_data(party, healer)
        self.table_view = []
        self._setup_table_view()
        self._setup_scroll_layer()

        self.cur_item = None
        self._update_rects_in_layer_rect_with_offset()

    def _fill_table_data(self, party, healer):

        for hero in party.values():  # in invclickbox staat er geen values() omdat party dan een list is.
            # laat de healer zelf niet in de lijst zien
            if hero != healer:
                # laad de hero subsprite
                hero_spr = pygame.image.load(hero.SPR).subsurface(32, 0, self.subsurw, self.subsurh).convert_alpha()
                hero_health = "HitPoints:     {} / {}".format(hero.cur_hp, hero.max_hp)
                self.table_data.append(
                    # row[0],    row[1],    row[2],  row[3], row[4]
                    [hero_spr, hero.NAM, hero_health, hero, None]
                )