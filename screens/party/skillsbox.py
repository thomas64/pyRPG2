
"""
class: SkillsBox
"""

import pygame

from .basebox import BaseBox


COLUMN1X = 50
COLUMN2X = 90
COLUMN3X = 190
COLUMN4X = 220
COLUMN5X = 260
COLUMNSY = 50
ROWHEIGHT = 32

TITLE = "Skills"
TOTALCOLUMNS = (('icon', COLUMN1X), ('text', COLUMN2X), ('text', COLUMN3X), ('text', COLUMN4X), ('text', COLUMN5X))


class SkillsBox(BaseBox):
    """
    Alle weergegeven informatie van alle skills van een hero.
    """
    def __init__(self, position, width, height):
        super().__init__(position, width, height)

        self.title = self.largefont.render(TITLE, True, self.fontcolor1).convert_alpha()
        self.rowheight = ROWHEIGHT
        self.total_columns = TOTALCOLUMNS
        self.column1x = COLUMN1X
        self.columnsy = COLUMNSY

    def update(self, hero, hovered_equipment_item):
        """
        Update eerst alle data.
        :param hero: de huidige geselecteerde hero uit partyscreen
        :param hovered_equipment_item: het item waar de muis overheen hovered in invclickbox
        """
        self.table_data = []
        for skill in hero.skills_tuple:
            if skill.positive_quantity():
                preview_value = self._get_difference(hero, hovered_equipment_item, skill.RAW)
                self.table_data.append(
                    # row[0],       row[1],           row[2],       row[3],  row[4],  row[5],     row[6]
                    [skill.ICON, skill.NAM + " :", str(skill.qty), None, skill.DESC, skill.ext, preview_value]
                )

        # maak dan een nieuwe tabel aan met de tekst en icons, maar dan gerendered.
        self.table_view = []
        for index, row in enumerate(self.table_data):
            self.table_view.append(list())
            self.table_view[index].append(pygame.image.load(row[0]).convert_alpha())
            self.table_view[index].append(self.normalfont.render(row[1], True, self._get_color(index)).convert_alpha())
            self.table_view[index].append(self.normalfont.render(row[2], True, self.fontcolor1).convert_alpha())
            self._set_color(row[5], self.table_view[index], 1)
            self._set_color(row[6], self.table_view[index], 2)

        if self.run_once:
            self.run_once = False
            self._setup_scroll_layer()
        # vul row[3] kolom. hierin staan de rects van row[1]. rect is voor muisklik.
        self._update_rects_in_layer_rect_with_offset()
