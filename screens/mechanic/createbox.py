
"""
class: CreateBox
"""

from components import ListBox
from constants import ColumnType
import inventoryitems

COLUMN1X = 0
COLUMN2X = 34

TOTALCOLUMNS = ((ColumnType.s_icon, COLUMN1X, "", ""),
                (ColumnType.text,   COLUMN2X, "Item", "Name:"))


class CreateBox(ListBox):
    """
    De box met alle mogelijk te creeren equipment.
    """
    def __init__(self, x, y, width, height, eqp_database):
        super().__init__(x, y, width, height)

        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X    # deze is voor de baseclass
        self.row_nr_with_rect = 2   # row[2]
        self.row_nr_with_obj = 3    # row[3]

        self.table_data = []
        self._fill_table_data(eqp_database)
        self.table_view = []
        self._setup_table_view()
        self._setup_scroll_layer()

        self.cur_item = None
        self._update_rects_in_layer_rect_with_offset()

    def _fill_table_data(self, eqp_database):

        for equipment_item in eqp_database:
            if equipment_item.value.get('cus'):
                equipment_obj = inventoryitems.factory_equipment_item(equipment_item)
                if equipment_obj.get_value_of('SKL'):
                    equipment_item_nam = "[" + equipment_obj.SKL.value + "] " + equipment_obj.NAM
                    if "Shield" in equipment_item_nam:
                        equipment_item_nam = equipment_obj.NAM
                else:
                    equipment_item_nam = equipment_obj.NAM
                self.table_data.append(
                    # row[0],                 row[1],      row[2],    row[3]
                    [equipment_obj.SPR, equipment_item_nam, None,   equipment_obj]
                )

    def mouse_hover(self, event):
        """
        :param event: pygame.MOUSEMOTION uit mechanic screen
        """
        for index, row in enumerate(self.table_data):
            if row[self.row_nr_with_rect].collidepoint(event.pos):
                self.cur_item = index
                return row[self.row_nr_with_obj].NAM, row[self.row_nr_with_obj].DESC
        return None, None
