
"""
class: Display
"""

import random

from components import MessageBox
from components import Parchment

from constants import GameState
from constants import SFX

from database import PouchItemDatabase

import inventoryitems

from .createbox import CreateBox
from .pouchbox import PouchBox


SOURCETITLE1 = "Stamina {}: {}"


class Display(Parchment):
    """
    ...
    """
    def __init__(self, engine, hero):
        super().__init__(engine, "Create", "Pouch")

        self.name = GameState.Shop

        self.main_title_pos_x = 1 / 16
        self.main_title_pos_y = 1 / 32
        self.source_title1 = SOURCETITLE1
        self.source_title1_pos_x = 1 / 16
        self.source_title1_pos_y = 75 / 100
        self.sub_title_pos_x = 5
        self.sub_title_pos_y1 = 15 / 100
        self.sub_title_pos_y2 = 17 / 100

        self.face_pos_x = 1 / 16
        self.face_pos_y = 3 / 16
        self.extra_face_size_x = 20
        self.extra_face_size_y = 0
        self.lines_next_to_face = 4
        self.small_line_height = 27

        self.leftbox_width = 3 / 16
        self.leftbox_height = 73 / 100
        self.leftbox_pos_x = 47 / 100
        self.leftbox_pos_y = 6 / 32
        self.rightbox_width = 3 / 16
        self.rightbox_height = 73 / 100
        self.rightbox_pos_x = 72 / 100
        self.rightbox_pos_y = 6 / 32
        self.infobox_width = 25 / 100
        self.infobox_height = 11 / 100
        self.infobox_pos_x = 1 / 16
        self.infobox_pos_y = 81 / 100

        self.cur_hero = hero
        self._init_face_and_text(self.cur_hero.FAC, self.cur_hero.alc.welcome_text(self.cur_hero.NAM))
        self._init_boxes()
        self._init_buttons()

    def _init_boxes(self):
        self._init_infobox()
        self._init_createbox()
        self._init_pouchbox()

    def _init_createbox(self):
        width = self.screen.get_width() * self.leftbox_width
        height = self.screen.get_height() * self.leftbox_height
        # zoek in de PouchItemDatabase naar de enum keys die eindigen op _pot of _flk en stop die allemaal in een list.
        # en zoek ook naar potions die juiste alc skill waarde hebben om gemaakt te kunnen worden.
        database = list()
        for itm in PouchItemDatabase:
            if itm.name[-4:] in ('_pot', '_flk') and self.cur_hero.alc.tot >= itm.value['alc']:
                database.append(itm)
        self.leftbox = CreateBox(self._set_x(self.leftbox_pos_x), self._set_y(self.leftbox_pos_y),
                                 int(width), int(height), database, self.cur_hero.alc)

    def _init_pouchbox(self):
        width = self.screen.get_width() * self.rightbox_width
        height = self.screen.get_height() * self.rightbox_height
        self.rightbox = PouchBox(self._set_x(self.rightbox_pos_x), self._set_y(self.rightbox_pos_y),
                                 int(width), int(height), self.engine.data.pouch)

    def update(self, dt):
        """
        :param dt: self.clock.tick(FPS)/1000.0
        """
        self.main_title = self.cur_hero.alc.NAM
        self.source_title1 = SOURCETITLE1.format(self.cur_hero.NAM, str(self.cur_hero.sta.cur))

    def _handle_leftbox_click(self, event):
        create_click, selected_potion = self.leftbox.mouse_click(event)
        if create_click:
            herbs = inventoryitems.factory_pouch_item(PouchItemDatabase.herbs)
            spices = inventoryitems.factory_pouch_item(PouchItemDatabase.spices)
            gemstones = inventoryitems.factory_pouch_item(PouchItemDatabase.gemstones)
            hrb_qty = self.engine.data.pouch.get_quantity(herbs)
            spc_qty = self.engine.data.pouch.get_quantity(spices)
            gms_qty = self.engine.data.pouch.get_quantity(gemstones)

            if selected_potion.HRB > hrb_qty or \
               selected_potion.SPC > spc_qty or \
               selected_potion.GMS > gms_qty:
                text = ["You do not have the right components",
                        "to create that {}.".format(selected_potion.NAM)]
                push_object = MessageBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.menu_cancel)
                self.engine.gamestate.push(push_object)
                return True
            elif self.cur_hero.sta.cur < self.cur_hero.alc.STA_COST:
                text = ["You do not have enough stamina",
                        "to create that {}.".format(selected_potion.NAM)]
                push_object = MessageBox(self.engine.gamestate, self.engine. audio, text, sound=SFX.menu_cancel)
                self.engine.gamestate.push(push_object)
                return True
            elif 'pouch is full' is False:  # todo, moet 'pouch is vol' hier? of in pouch?
                self.engine.audio.play_sound(SFX.menu_cancel)
                return True

            self.engine.data.pouch.remove(herbs, selected_potion.HRB, force=True)  # want kan ook 0 zijn.
            self.engine.data.pouch.remove(spices, selected_potion.SPC, force=True)
            self.engine.data.pouch.remove(gemstones, selected_potion.GMS, force=True)

            self.cur_hero.sta.cur -= self.cur_hero.alc.STA_COST

            rnd_percentage = random.randint(1, 100)
            potion_chance = self.cur_hero.alc.get_percentage(selected_potion.ALC)
            if potion_chance >= rnd_percentage:
                text = ["{} successfully created.".format(selected_potion.NAM)]
                self.engine.data.pouch.add(selected_potion)
                push_object = MessageBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.message)
                self.engine.gamestate.push(push_object)
            else:
                text = ["Failed to create a {}.".format(selected_potion.NAM)]
                push_object = MessageBox(self.engine.gamestate, self.engine.audio, text, sound=SFX.menu_cancel)
                self.engine.gamestate.push(push_object)

            self._init_boxes()
            return True
        return False
