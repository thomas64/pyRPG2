
"""
class: KnownBox
"""

from components import ListBox
from constants import ColumnType

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 234

TOTALCOLUMNS = ((ColumnType.s_icon, COLUMN1X, "", ""),
                (ColumnType.text,   COLUMN2X, "Spell", "Name:"),
                (ColumnType.text,   COLUMN3X, "Current", "Rank:"))


class KnownBox(ListBox):
    """
    De box waarin de spells per persoon te zien zijn.
    Deze class bevat heel veel van sellbox uit shop.
    """
    def __init__(self, x, y, width, height, hero):
        super().__init__(x, y, width, height)

        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X    # deze is voor de baseclass
        self.row_nr_with_rect = 5   # row[5]
        self.row_nr_with_obj = 4    # row[4]

        self.table_data = []
        self._fill_table_data(hero)
        self.table_view = []
        self._setup_table_view()
        self._setup_scroll_layer()

        self.cur_item = None
        self._update_rects_in_layer_rect_with_offset()

    def _fill_table_data(self, hero):

        for spell in hero.scl.get_all_spells():
            self.table_data.append(
                # row[0],       row[1],    row[2],        row[3],   row[4], row[5]
                [spell.ICON, spell.NAM, str(spell.qty), spell.DESC, spell, None]
            )
