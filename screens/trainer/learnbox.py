
"""
class: LearnBox
"""

from components import ListBox

COLUMN1X = 0
COLUMN2X = 34
COLUMN3X = 234
COLUMN4X = 284
COLUMN5X = 334

TOTALCOLUMNS = (('icon', COLUMN1X), ('text', COLUMN2X), ('text', COLUMN3X), ('text', COLUMN4X), ('text', COLUMN5X))


class LearnBox(ListBox):
    """
    De box waarin de te leren skills te zien zijn.
    Deze class is bijna identiek aan LearnBox van School.
    """
    def __init__(self, x, y, width, height, skilltype_list, hero):
        super().__init__(x, y, width, height)

        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X    # deze is voor de baseclass
        self.row_nr_with_rect = 6   # row[6]
        self.row_nr_with_obj = 5    # row[5]

        self.table_data = []
        self._fill_table_data(skilltype_list, hero)
        self.table_view = []
        self._setup_table_view()
        self._setup_scroll_layer()

        self.cur_item = None
        self._update_rects_in_layer_rect_with_offset()

    def _fill_table_data(self, skilltype_list, hero):
        for skill in hero.skills_tuple:
            if skill.RAW in skilltype_list:
                next_level = str(skill.nxt_lev)
                gold_cost = str(skill.gold_cost)
                xp_cost = str(skill.xp_cost)
                self.table_data.append(
                    #  row[0],    row[1],     row[2],     row[3],   row[4], row[5], row[6],
                    [skill.ICON, skill.NAM, next_level, gold_cost, xp_cost, skill,  None]
                )
