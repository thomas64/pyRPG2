
"""
class: LearnedBox
"""

import pygame

from components import ListBox

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 306

TOTALCOLUMNS = (('icon', COLUMN1X), ('text', COLUMN2X), ('text', COLUMN3X))


class LearnedBox(ListBox):
    """
    De box waarin de spells per persoon te zien zijn.
    Deze class bevat heel veel van sellbox uit shop.
    """
    def __init__(self, x, y, width, height, hero):
        super().__init__(x, y, width, height)

        self.table_data = []
        self._fill_table_data(hero)
        self.table_view = []
        self._setup_table_view()
        self._setup_scroll_layer()

        self.background = pygame.Surface((width, self.layer_height))
        self.background.fill(self.colorkey)
        self.background = self.background.convert()

        self.cur_item = None

        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X    # deze is voor de baseclass
        self.row_nr_with_rect = 7   # row[7]
        self.row_nr_with_obj = 6    # row[6]
        self._update_rects_in_layer_rect_with_offset(self.row_nr_with_rect)

    def _fill_table_data(self, hero):

        for spell in hero.scl.get_all_spells():
            self.table_data.append(
                # row[0],       row[1],    row[2],        row[3],     row[4],    row[5], row[6], row[7]
                [spell.ICON, spell.NAM, str(spell.qty), spell.DESC, spell.COL, spell.ROW, spell, None]
            )

    def _setup_table_view(self):
        """
        Zet table_data om in een visuele weergave.
        """
        normalfont = pygame.font.SysFont(self.font, self.fontsize)

        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(pygame.image.load(row[0]).subsurface(row[4], row[5], 32, 32).convert_alpha())
            self.table_view[index].append(normalfont.render(row[1], True, self.fontcolor).convert_alpha())
            self.table_view[index].append(normalfont.render(row[2], True, self.fontcolor).convert_alpha())
