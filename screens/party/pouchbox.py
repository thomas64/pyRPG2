
"""
class: PouchBox
"""

import pygame

from .basebox import BaseBox


COLUMN1X = 25
COLUMN2X = COLUMN1X + 40
COLUMN3X = COLUMN2X + 130
COLUMNSY = 50
ROWHEIGHT = 30

TITLE = "Pouch"
TOTALCOLUMNS = (('icon', COLUMN1X), ('text', COLUMN2X), ('text', COLUMN3X))


class PouchBox(BaseBox):
    """
    Alle weergegeven informatie van alle pouchitems van de party.
    """
    def __init__(self, position, width, height):
        super().__init__(position, width, height)

        self.title = self.largefont.render(TITLE, True, self.fontcolor1).convert_alpha()
        self.rowheight = ROWHEIGHT
        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X
        self.columnsy = COLUMNSY

    def update(self, pouch):
        """
        Update eerst alle data.
        :param pouch:
        """
        self.view_matrix = []
        self.data_matrix = []
        for index, pouch_item in enumerate(pouch.get_all_pouch_items()):
            self.view_matrix.append(
                [pygame.image.load(pouch_item.SPR).convert_alpha(),
                 self.normalfont.render(pouch_item.NAM+" :", True, self._get_color(index)).convert_alpha(),
                 self.normalfont.render(str(pouch_item.qty), True, self.fontcolor1).convert_alpha()
                 ]
            )
            self.data_matrix.append([pouch_item, None, pouch_item.DESC])

        if self.run_once:
            self.run_once = False
            self._setup_scroll_layer()
        # vul datamatrix[X][1]. hierin staan de rects van viewmatrix[X][1].NAM. rect is voor muisklik.
        self._update_rects_in_layer_rect_with_offset()
