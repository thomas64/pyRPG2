
"""
class: SpellsBox
"""

import pygame

from .basebox import BaseBox


COLUMN1X = 50
COLUMN2X = 90
COLUMN3X = 220
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

        self.table_data = []
        for spell in hero.scl.get_all_spells():
            self.table_data.append(
                # row[0],       row[1],           row[2],     row[3],  row[4],     row[5],    row[6]
                [spell.ICON, spell.NAM + " :", str(spell.qty), None, spell.DESC, spell.COL, spell.ROW]
            )

        # maak dan een nieuwe tabel aan met de tekst en icons, maar dan gerendered.
        self.table_view = []
        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(pygame.image.load(row[0]).subsurface(row[5], row[6], 32, 32).convert())
            self.table_view[index].append(self.normalfont.render(row[1], True, self._get_color(index)).convert_alpha())
            self.table_view[index].append(self.normalfont.render(row[2], True, self.fontcolor1).convert_alpha())

        if self.run_once:
            self.run_once = False
            self._setup_scroll_layer()
        # vul row[3] kolom. hierin staan de rects van row[1]. rect is voor muisklik.
        self._update_rects_in_layer_rect_with_offset()
