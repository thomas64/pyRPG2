
"""
class: PouchBox
"""

from components import ListBox

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 70

TOTALCOLUMNS = (('icon', COLUMN1X, "", ""),
                ('text', COLUMN2X, "", ""),
                ('text', COLUMN3X, "", ""))


class PouchBox(ListBox):
    """
    De box waar de resources uit je pouch in te zien is.
    """
    def __init__(self, x, y, width, height, pouch):
        super().__init__(x, y, width, height)

        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X    # deze is voor de baseclass
        self.row_nr_with_rect = 4   # row[4]
        self.row_nr_with_obj = 3    # row[3]

        self.table_data = []
        self._fill_table_data(pouch)
        self.table_view = []
        self._setup_table_view()
        self._setup_scroll_layer()

        self.cur_item = None
        self._update_rects_in_layer_rect_with_offset()

    def _fill_table_data(self, pouch):

        for resource_item_obj in pouch.get_all_resource_items():
            self.table_data.append(
                # row[0],                       row[1],                 row[2],                 row[3],      row[4]
                [resource_item_obj.SPR, str(resource_item_obj.qty), resource_item_obj.NAM, resource_item_obj, None]
            )
