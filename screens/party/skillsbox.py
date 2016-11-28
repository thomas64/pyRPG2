
"""
class: SkillsBox
"""

import pygame

from .basebox import BaseBox


COLUMN1X = 40   # icon
COLUMN2X = 80   # naam
COLUMN3X = 180  # base stat
COLUMN4X = 200  # ext value
COLUMN5X = 240  # tot stat
COLUMN6X = 270  # preview value
COLUMNSY = 50
ROWHEIGHT = 32

TITLE = "Skills"
TOTALCOLUMNS = (('icon', COLUMN1X), ('text', COLUMN2X), ('text', COLUMN3X), ('text', COLUMN4X), ('text', COLUMN5X),
                                                                                                ('text', COLUMN6X))


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
        index = 0
        for skill in hero.skills_tuple:
            if skill.positive_quantity():
                self.view_matrix.append(list())  # deze lege lijst moest eerst vanwege de self._set_color() met [index]
                preview_value = self._get_difference(hero, hovered_equipment_item, skill.RAW)

                self.view_matrix[index].append(
                    pygame.image.load(skill.ICON).convert_alpha())
                self.view_matrix[index].append(
                    self.normalfont.render(skill.NAM + " :", True, self._get_color(index)).convert_alpha())
                self.view_matrix[index].append(
                    self.normalfont.render(str(skill.qty), True, self.fontcolor1).convert_alpha())
                self.view_matrix[index].append(
                    self._set_color(skill.ext, 1))
                self.view_matrix[index].append(
                    self.normalfont.render("(" + str(skill.tot) + ")", True, self.fontcolor1).convert_alpha())
                self.view_matrix[index].append(
                    self._set_color(preview_value, 2))

                self.data_matrix.append([skill, None])
                index += 1

        if self.run_once:
            self.run_once = False
            self._setup_scroll_layer()
        # vul datamatrix[X][1]. hierin staan de rects van viewmatrix[X][1].NAM. rect is voor muisklik.
        self._update_rects_in_layer_rect_with_offset()
