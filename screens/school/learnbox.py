
"""
class: LearnBox
"""

import inspect

import pygame

from characters import spells
from components import ListBox

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 234
COLUMN4X = 284
COLUMN5X = 334

TOTALCOLUMNS = (('icon', COLUMN1X), ('text', COLUMN2X), ('text', COLUMN3X), ('text', COLUMN4X), ('text', COLUMN5X))


class LearnBox(ListBox):
    """
    ...
    """
    def __init__(self, x, y, width, height, schooltype_list, hero):
        super().__init__(x, y, width, height)

        self.table_data = []
        self._fill_table_data(schooltype_list, hero)
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

    def _fill_table_data(self, schooltype_list, hero):
        # zoek the classes in module ``spells`` that inherit from ``Spell``
        for name, obj in inspect.getmembers(spells):
            if hasattr(obj, "__bases__") and spells.Spell in obj.__bases__:
                # maak objecten van alle classen, de 1 is de benodigde quantity parameter van Spell.
                # 1 is just random. de daadwerkelijke juiste quantity wordt later gezet.
                spell = obj(1)
                if spell.SCL in schooltype_list:
                    spell.qty = hero.scl.get_qty_of_spell(spell.RAW)    # .qty kan hier dus 0 zijn
                    next_level = str(spell.nxt_lev)                     # in dat geval, gebruik hier 1
                    gold_cost = str(spell.gold_cost)                    # gold_cost kijkt wat de prijs is voor 1 vanaf 0
                    xp_cost = str(spell.xp_cost)                        # idem voor xp_cost
                    self.table_data.append(
                        #  row[0],    row[1],     row[2],    row[3], row[4], row[5], row[6],
                        [spell.ICON, spell.NAM, spell.COL, spell.ROW, spell, None, next_level,
                         # row[7],   row[8]
                         gold_cost, xp_cost]
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
            self.table_view[index].append(normalfont.render(row[6], True, self.fontcolor).convert_alpha())
            self.table_view[index].append(normalfont.render(row[7], True, self.fontcolor).convert_alpha())
            self.table_view[index].append(normalfont.render(row[8], True, self.fontcolor).convert_alpha())

    def mouse_click(self, event):
        """
        :param event: pygame.MOUSEBUTTONDOWN uit school display.
        """
        for index, row in enumerate(self.table_data):
            if row[5].collidepoint(event.pos):
                self.cur_item = index
                selected_spell = row[4]
                # selected_spell heeft dus eventueel .qty = 0
                return True, selected_spell

        return False, None
