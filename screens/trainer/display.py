
"""
class: Display
"""

import pygame

from components import ConfirmBox
from components import MessageBox
from components import Parchment

from constants import GameState
from constants import SFX

from database import TrainerDatabase
from database import PouchItemDatabase
import inventoryitems

from .knownbox import KnownBox
from .trainbox import TrainBox
from screens.school.selector import Selector


SOURCETITLE1 = "Gold: {}"
SOURCETITLE2 = "XP Remaining: {}"


class Display(Parchment):
    """
    ...
    """
    def __init__(self, engine, skilltype_list, face):
        super().__init__(engine, "Train", "Known")

        self.skilltypes = skilltype_list
        self.subtype_list = list(self.engine.data.party.values())
        self.subtype = self.subtype_list[0]

        self.name = GameState.Shop

        self.main_title_pos_x = 1 / 16
        self.main_title_pos_y = 1 / 32
        self.source_title1 = SOURCETITLE1
        self.source_title1_pos_x = 1 / 16
        self.source_title1_pos_y = 39 / 64
        self.source_title2 = SOURCETITLE2
        self.source_title2_pos_x = 1 / 16
        self.source_title2_pos_y = 42 / 64
        self.sub_title_pos_x = 5
        self.sub_title_pos_y1 = 15 / 100
        self.sub_title_pos_y2 = 17 / 100

        self.face_pos_x = 1 / 16
        self.face_pos_y = 3 / 16
        self.extra_face_size_x = 20
        self.extra_face_size_y = 20
        self.lines_next_to_face = 3
        self.small_line_height = 30

        self.leftbox_width = 9 / 32
        self.leftbox_height = 24 / 32
        self.leftbox_pos_x = 2 / 5
        self.leftbox_pos_y = 6 / 32
        self.rightbox_width = 7 / 32
        self.rightbox_height = 24 / 32
        self.rightbox_pos_x = 23 / 32
        self.rightbox_pos_y = 6 / 32
        self.infobox_width = 8 / 32
        self.infobox_height = 7 / 32
        self.infobox_pos_x = 2 / 32
        self.infobox_pos_y = 23 / 32

        self.selector_pos_x = 2 / 32
        self.selector_pos_y = 18 / 32
        self.selector_width = 36

        self.gold_amount = None
        self.gold_object = inventoryitems.factory_pouch_item(PouchItemDatabase.gold)
        self.xp_amount = None

        self._init_face_and_text(face, TrainerDatabase.welcome_text())
        self._init_selectors()
        self._init_boxes()
        self._init_buttons()

        self._reset_vars()

    def _reset_vars(self):
        self.train_click = False
        self.selected_skill = None
        self.gold_cost = 0
        self.xp_cost = 0
        self.confirm_box = None

    def _init_selectors(self):
        for index, hero in enumerate(self.subtype_list):
            self.selectors.add(Selector(self._set_x(self.selector_pos_x) + index * self.selector_width,
                                        self._set_y(self.selector_pos_y), hero))

    def _init_boxes(self):
        self._init_infobox()
        self._init_trainbox()
        self._init_knownbox()

    def _init_trainbox(self):
        width = self.screen.get_width() * self.leftbox_width
        height = self.screen.get_height() * self.leftbox_height
        self.leftbox = TrainBox(self._set_x(self.leftbox_pos_x), self._set_y(self.leftbox_pos_y),
                                int(width), int(height), self.skilltypes, self.subtype)

    def _init_knownbox(self):
        width = self.screen.get_width() * self.rightbox_width
        height = self.screen.get_height() * self.rightbox_height
        self.rightbox = KnownBox(self._set_x(self.rightbox_pos_x), self._set_y(self.rightbox_pos_y),
                                 int(width), int(height), self.subtype)

    def on_enter(self):
        """
        Wanneer deze state op de stack komt, voer dit uit.
        Handel af als er een train confirmbox is geweest.
        """
        if self.train_click:
            choice = self.confirm_box.cur_item
            yes = self.confirm_box.TOPINDEX
            if choice == yes:
                self.engine.audio.play_sound(SFX.upgrade)
                self.engine.data.pouch.remove(self.gold_object, self.gold_cost)
                self.subtype.exp.rem -= self.xp_cost  # subtype is een hero
                # hier staat selected_skill eventueel nog op. deze zin is kopie van school, is hij wel van toepassing?
                self.selected_skill.upgrade()
                self._init_boxes()
            else:
                self.engine.audio.play_sound(SFX.menu_select)

            self._reset_vars()

    def multi_input(self, key_input, mouse_pos, dt):
        """
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        if self.engine.debug_mode:
            # todo, weghalen uiteindelijk. cheat voor xp erbij ctrl+
            if key_input[pygame.K_LCTRL] or key_input[pygame.K_RCTRL]:
                if key_input[pygame.K_KP_PLUS]:
                    self.subtype.gain_experience(1)
                elif key_input[pygame.K_KP_MINUS]:
                    self.subtype.gain_experience(-1)

    def update(self, dt, gamestate, audio):
        """
        Update de selector border color.
        Update de gold en xp quantity.
        :param dt: self.clock.tick(FPS)/1000.0
        :param gamestate:
        :param audio:
        """
        for selector in self.selectors:
            selector.update(self.subtype)
        self.gold_amount = self.engine.data.pouch.get_quantity(self.gold_object)
        self.xp_amount = self.subtype.exp.rem
        self.main_title = self.subtype.NAM
        self.source_title1 = SOURCETITLE1.format(str(self.gold_amount))
        self.source_title2 = SOURCETITLE2.format(str(self.xp_amount))

    def _handle_leftbox_click(self, event):
        self.train_click, self.selected_skill = self.leftbox.mouse_click(event)
        # selected_skill is hier eventueel .qty = 0. deze zin is kopie. wel van toepassing?
        if self.train_click:
            self.gold_cost = self.selected_skill.gold_cost
            self.xp_cost = self.selected_skill.xp_cost
            succes, text = self.selected_skill.is_able_to_train(self.xp_amount, self.gold_amount)
            if succes:
                text = ["{}: {}  --> {}.".format(self.selected_skill.NAM,
                                                 self.selected_skill.qty, self.selected_skill.qty + 1),
                        "Are you sure you wish to train the",
                        "skill {} for {} XP and {} gold?".format(self.selected_skill.NAM,
                                                                 self.xp_cost, self.gold_cost),
                        "",
                        "Yes",
                        "No"]
                self.confirm_box = ConfirmBox(text)
                self.engine.gamestate.push(self.confirm_box)
            else:
                push_object = MessageBox(text, sound=SFX.menu_cancel)
                self.engine.gamestate.push(push_object)
                self._reset_vars()
            return True
        return False
