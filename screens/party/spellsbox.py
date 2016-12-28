
"""
class: SpellsBox
"""

import pygame

from .basebox import BaseBox


COLUMN1X = 25
COLUMN2X = COLUMN1X + 40
COLUMN3X = COLUMN2X + 130
COLUMNSY = 50
ROWHEIGHT = 34

TITLE = "Spells"
TOTALCOLUMNS = (('icon', COLUMN1X), ('text', COLUMN2X), ('text', COLUMN3X))


class SpellsBox(BaseBox):
    """
    Alle weergegeven informatie van alle spells van een hero.
    """
    def __init__(self, position, width, height):
        super().__init__(position, width, height)

        self.title = None
        self.rowheight = ROWHEIGHT
        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X
        self.columnsy = COLUMNSY

    def update(self, hero):
        """
        Update eerst alle data.
        :param hero: de huidige geselecteerde hero uit partyscreen
        """
        self.title = self.largefont.render(
                                    "{} {}".format(hero.scl.NAM.value, TITLE), True, self.fontcolor1).convert_alpha()
        self.view_matrix = []
        self.data_matrix = []
        for index, spell in enumerate(hero.scl.get_all_spells()):
            self.view_matrix.append(
                [pygame.image.load(spell.ICON).subsurface(spell.COL, spell.ROW, 32, 32).convert_alpha(),
                 self.normalfont.render(spell.NAM + " :", True, self._get_color(index)).convert_alpha(),
                 self.normalfont.render(str(spell.qty), True, self.fontcolor1).convert_alpha()
                 ]
            )
            self.data_matrix.append([spell, None, spell.DESC])

        if self.run_once:
            self.run_once = False
            self._setup_scroll_layer()
        # vul datamatrix[X][1]. hierin staan de rects van viewmatrix[X][1].NAM. rect is voor muisklik.
        self._update_rects_in_layer_rect_with_offset()
