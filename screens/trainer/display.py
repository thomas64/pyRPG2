
"""
class: Display
"""

import pygame

from database import TrainerDatabase

import screens.school.display as scl
from .knownbox import KnownBox
from .learnbox import LearnBox

FONTCOLOR = pygame.Color("black")
LEARNTITLE = "Train"
OBJECTDATABASE = TrainerDatabase
OBJECTTYPE = "skill"


class Display(scl.Display):
    """
    ...
    """
    def __init__(self, engine, schooltype_list, face):
        super().__init__(engine, schooltype_list, face)

        self.learn_title = self.largefont.render(LEARNTITLE, True, FONTCOLOR).convert_alpha()

        self.object_type = OBJECTTYPE

    def _init_database(self):
        self.object_database = OBJECTDATABASE

    def _init_knownbox(self):
        width = self.screen.get_width() * scl.KNOWNBOXWIDTH
        height = self.screen.get_height() * scl.KNOWNBOXHEIGHT + scl.EXTRAHEIGHT
        self.knownbox = KnownBox(self._set_x(scl.KNOWNBOXPOSX), self._set_y(scl.KNOWNBOXPOSY), int(width), int(height),
                                 self.selected_hero)

    def _init_learnbox(self):
        width = self.screen.get_width() * scl.LEARNBOXWIDTH
        height = self.screen.get_height() * scl.LEARNBOXHEIGHT + scl.EXTRAHEIGHT
        self.learnbox = LearnBox(self._set_x(scl.LEARNBOXPOSX), self._set_y(scl.LEARNBOXPOSY), int(width), int(height),
                                 self.schooltype_list, self.selected_hero)

    def _on_enter2(self):
        self.selected_spell.upgrade()

    def _handle_learn_box_click2(self):
        return self.selected_spell.is_able_to_train(self.xp_amount, self.gold_amount)
