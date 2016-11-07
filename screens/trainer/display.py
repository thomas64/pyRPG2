
"""
class: Display
"""

import pygame

from components import MessageBox
from constants import SFX
from database import TrainerDatabase
from database import PouchItemDatabase
from inventoryitems import PouchItem

import screens.school.display as scl
from .knownbox import KnownBox
from .learnbox import LearnBox

OBJECTTYPE = "skill"


class Display(scl.Display):
    """
    ...
    """
    def __init__(self, engine, schooltype_list, face):
        super().__init__(engine, schooltype_list, face)

        self.object_type = OBJECTTYPE

    def _init_face(self, face):
        """
        Deze is er alleen vanwege TrainerDatabase. Andere manier mogelijk?
        """
        face_image = pygame.image.load(face).convert_alpha()
        self.background.blit(face_image, (self._set_x(scl.FACEPOSX), self._set_y(scl.FACEPOSY)))

        for index, line in enumerate(TrainerDatabase.welcome_text()):
            rline = self.smallfont.render(line, True, scl.FONTCOLOR).convert_alpha()
            if index < scl.LINESNEXTTOFACE:
                self.background.blit(rline,
                                     (self._set_x(scl.FACEPOSX) + face_image.get_width() + scl.EXTRAFACESIZE,
                                      self._set_y(scl.FACEPOSY) + scl.EXTRAFACESIZE + index * scl.SMALLLINEHEIGHT))
            else:
                self.background.blit(rline,
                                     (self._set_x(scl.FACEPOSX),
                                      self._set_y(scl.FACEPOSY) + scl.EXTRAFACESIZE + index * scl.SMALLLINEHEIGHT))

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

    def on_enter(self):
        """
        Wanneer deze state op de stack komt, voer dit uit.
        Handel af als er een learn confirmbox is geweest.
        """

        # todo, ander icoontje voor wizard.
        # todo, upgraden wanneer het niet kan (-1) implementeren.

        if self.learn_click:
            choice = self.confirm_box.cur_item
            yes = self.confirm_box.TOPINDEX
            if choice == yes:
                success, text = self.selected_spell.upgrade()
                if success:
                    self.engine.audio.play_sound(SFX.scroll)
                    gold = PouchItem(**PouchItemDatabase.gold.value)
                    self.engine.data.pouch.remove(gold, self.gold_cost)
                    self.selected_hero.exp.rem -= self.xp_cost
                    self._init_boxes()
                else:
                    self.engine.audio.play_sound(SFX.cancel)
                    push_object = MessageBox(self.engine.gamestate, text, scr_capt=self.confirm_box.scr_capt)
                    self.engine.gamestate.push(push_object)
            else:
                self.engine.audio.play_sound(SFX.menu_select)

            self._reset_vars()
