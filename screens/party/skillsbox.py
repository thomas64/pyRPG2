
"""
class: SkillsBox
"""

import pygame

from constants import ColumnType

from .basebox import BaseBox


COLUMN1X = 30              # icon
COLUMN2X = COLUMN1X + 40   # naam
COLUMN3X = COLUMN2X + 100  # base stat
COLUMN4X = COLUMN3X + 20   # ext value
COLUMN5X = COLUMN4X + 30   # preview value
COLUMN6X = COLUMN5X + 30   # tot stat
COLUMNSY = 50
ROWHEIGHT = 32

TITLE = "Skills"
TOTALCOLUMNS = ((ColumnType.icon, COLUMN1X),
                (ColumnType.text, COLUMN2X),
                (ColumnType.text, COLUMN3X),
                (ColumnType.text, COLUMN4X),
                (ColumnType.text, COLUMN5X),
                (ColumnType.text, COLUMN6X))


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
        self.view_matrix = []
        self.data_matrix = []
        index = 0  # vanwege de if in deze for loop. hij moet dan niet doortellen.
        for skill in hero.skills_tuple:
            if skill.positive_quantity():
                preview_value = self._get_difference(hero, hovered_equipment_item, skill.RAW)
                self.view_matrix.append(
                    [pygame.image.load(skill.ICON).convert_alpha(),
                     self.normalfont.render(skill.NAM + " :", True, self._get_color(index)).convert_alpha(),
                     self.normalfont.render(str(skill.qty), True, self.fontcolor1).convert_alpha(),
                     self._set_color(skill.ext, 1),
                     self._set_color(preview_value, 2),
                     self.normalfont.render(str(skill.tot), True, self.fontcolor1).convert_alpha()
                     ]
                )
                self.data_matrix.append([skill, None, skill.DESC])
                index += 1

        if self.run_once:
            self.run_once = False
            self._setup_scroll_layer()
        # vul datamatrix[X][1]. hierin staan de rects van viewmatrix[X][1].NAM. rect is voor muisklik.
        self._update_rects_in_layer_rect_with_offset()
