
"""
class: KnownBox
"""

from components import ListBox

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 234

TOTALCOLUMNS = (('icon', COLUMN1X), ('text', COLUMN2X), ('text', COLUMN3X))


class KnownBox(ListBox):
    """
    De box waarin de skills per persoon te zien zijn.
    Deze class is bijna identiek aan KnownBox van School.
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

        for skill in hero.skills_tuple:
            if skill.positive_quantity():
                self.table_data.append(
                    # row[0],       row[1],    row[2],        row[3],  row[4], row[5]
                    [skill.ICON, skill.NAM, str(skill.qty), skill.DESC, skill, None]
                )
