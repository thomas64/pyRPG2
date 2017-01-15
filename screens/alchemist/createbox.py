
"""
class: CreateBox
"""

from components import ListBox
from constants import ColumnType
import inventoryitems

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 200

TOTALCOLUMNS = ((ColumnType.icon, COLUMN1X, "", ""),
                (ColumnType.text, COLUMN2X, "Potion", "Name:"),
                (ColumnType.text, COLUMN3X, "Chance of", "Success:"))


class CreateBox(ListBox):
    """
    De box met alle mogelijk te manufacturingen potions.
    """
    def __init__(self, x, y, width, height, potion_database, hero_alc_skill):
        super().__init__(x, y, width, height)

        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X    # deze is voor de baseclass
        self.row_nr_with_rect = 3   # row[3]
        self.row_nr_with_obj = 4    # row[4]

        self.table_data = []
        self._fill_table_data(potion_database, hero_alc_skill)
        self.table_view = []
        self._setup_table_view()
        self._setup_scroll_layer()

        self.cur_item = None
        self._update_rects_in_layer_rect_with_offset()

    def _fill_table_data(self, potion_database, hero_alc_skill):

        for potion in potion_database:
            potion_obj = inventoryitems.factory_pouch_item(potion)
            percentage = str(hero_alc_skill.get_percentage(potion_obj.ALC)) + " %"
            self.table_data.append(
                # row[0],            row[1],       row[2],    row[3],   row[4]
                [potion_obj.SPR, potion_obj.NAM, percentage,   None,   potion_obj]
            )
