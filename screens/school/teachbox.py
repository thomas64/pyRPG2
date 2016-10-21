
"""
class: TeachBox
"""

import inspect

import pygame

from characters import spells
from components import ListBox

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 200
COLUMN4X = 350

TOTALCOLUMNS = (('icon', COLUMN1X), ('text', COLUMN2X), ('text', COLUMN3X), ('text', COLUMN4X))


class TeachBox(ListBox):
    """
    ...
    """
    def __init__(self, x, y, width, height, schooltype_list):
        super().__init__(x, y, width, height)

        self.table_data = []
        self._fill_table_data(schooltype_list)
        self.table_view = []
        self._setup_table_view()
        self._setup_scroll_layer()

        self.background = pygame.Surface((width, self.layer_height))
        self.background.fill(self.colorkey)
        self.background = self.background.convert()

        self.cur_item = None

        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X    # deze is voor de baseclass
        self.row_nr_with_rect = 5   # row[5]
        self.row_nr_with_obj = 4    # row[4]
        self._update_rects_in_layer_rect_with_offset(self.row_nr_with_rect)

    def _fill_table_data(self, schooltype_list):

        # zoek the classes in module ``spells`` that inherit from ``Spell``
        for name, obj in inspect.getmembers(spells):
            if hasattr(obj, "__bases__") and spells.Spell in obj.__bases__:
                # maak objecten van alle classen
                spell = obj(1)

                if spell.SCL in schooltype_list:
                    self.table_data.append(
                        #  row[0],    row[1],     row[2],    row[3], row[4], row[5]
                        [spell.ICON, spell.NAM, spell.COL, spell.ROW, spell, None]
                    )
        # sorteer de lijst
        self.table_data.sort(key=lambda xx: xx[4].SRT)

    def _setup_table_view(self):
        """
        Zet table_data om in een visuele weergave.
        """
        normalfont = pygame.font.SysFont(self.font, self.fontsize)

        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(pygame.image.load(row[0]).subsurface(row[2], row[3], 32, 32).convert_alpha())
            self.table_view[index].append(normalfont.render(row[1], True, self.fontcolor).convert_alpha())
            self.table_view[index].append(normalfont.render(row[1], True, self.fontcolor).convert_alpha())
            self.table_view[index].append(normalfont.render(row[1], True, self.fontcolor).convert_alpha())
