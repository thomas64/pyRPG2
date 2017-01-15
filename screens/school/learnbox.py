
"""
class: LearnBox
"""

import inspect

from characters import spells
from components import ListBox
from constants import ColumnType

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 234
COLUMN4X = 284
COLUMN5X = 334

TOTALCOLUMNS = ((ColumnType.s_icon, COLUMN1X, "", ""),
                (ColumnType.text,   COLUMN2X, "Spell", "Name:"),
                (ColumnType.text,   COLUMN3X, "Next", "Rank:"),
                (ColumnType.text,   COLUMN4X, "Gold", "Cost:"),
                (ColumnType.text,   COLUMN5X, "XP", "Cost:"))


class LearnBox(ListBox):
    """
    ...
    """
    def __init__(self, x, y, width, height, schooltype_list, hero):
        super().__init__(x, y, width, height)

        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X    # deze is voor de baseclass
        self.row_nr_with_rect = 6   # row[6]
        self.row_nr_with_obj = 5    # row[5]

        self.table_data = []
        self._fill_table_data(schooltype_list, hero)
        self.table_view = []
        self._setup_table_view()
        self._setup_scroll_layer()

        self.cur_item = None
        self._update_rects_in_layer_rect_with_offset()

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
                        #  row[0],    row[1],     row[2],    row[3],    row[4], row[5], row[6],
                        [spell.ICON, spell.NAM, next_level, gold_cost, xp_cost, spell,  None]
                    )
        # sorteer de lijst
        self.table_data.sort(key=lambda xx: xx[self.row_nr_with_obj].SRT)
