
"""
class: CreateBox
"""

from components import ListBox
from inventoryitems import PouchItem

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 200

TOTALCOLUMNS = (('icon', COLUMN1X), ('text', COLUMN2X), ('text', COLUMN3X))


class CreateBox(ListBox):
    """
    De box met alle mogelijk te manufacturingen potions.
    """
    def __init__(self, x, y, width, height, potion_database):
        super().__init__(x, y, width, height)

        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X    # deze is voor de baseclass
        self.row_nr_with_rect = 3   # row[3]
        self.row_nr_with_obj = 4    # row[4]

        self.table_data = []
        self._fill_table_data(potion_database)
        self.table_view = []
        self._setup_table_view()
        self._setup_scroll_layer()

        self.cur_item = None
        self._update_rects_in_layer_rect_with_offset()

    def _fill_table_data(self, potion_database):

        for potion in potion_database:
            potion_obj = PouchItem(**potion.value)
            self.table_data.append(
                # row[0],            row[1],    row[2], row[3],   row[4]
                [potion_obj.SPR, potion_obj.NAM, "0%",   None,   potion_obj]
            )
