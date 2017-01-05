
"""
class: Display
"""

import random

import pygame

from components import Button
from components import MessageBox
from components import Parchment
from components import TextBox

from constants import GameState
from constants import Keys
from constants import SFX

from database import PouchItemDatabase

import inventoryitems

from .createbox import CreateBox
from .pouchbox import PouchBox


BACKGROUNDCOLOR = pygame.Color("black")
COLORKEY = pygame.Color("white")
FONTCOLOR = pygame.Color("black")

CREATETITLE = "Create"
POUCHTITLE = "Pouch"
TITLEPOSX = 1/16
TITLEPOSY = 1/32
FACEPOSX = 1/16
FACEPOSY = 3/16
EXTRAFACESIZEX = 20
EXTRAFACESIZEY = 0
LINESNEXTTOFACE = 4
SMALLLINEHEIGHT = 27

STATITLE = "Stamina {}: "
STATITLEPOSX = 1/16
STATITLEPOSY = 75/100

CREATEBOXWIDTH = 3/16
CREATEBOXHEIGHT = 73/100
CREATEBOXPOSX = 47/100
CREATEBOXPOSY = 6/32

POUCHBOXWIDTH = 3/16     # van het scherm
POUCHBOXHEIGHT = 73/100
POUCHBOXPOSX = 72/100     # x op 72/100 van het scherm
POUCHBOXPOSY = 6/32

EXTRAHEIGHT = 0         # zodat de laatste item er voor helft op komt

INFOBOXWIDTH = 25/100
INFOBOXHEIGHT = 11/100
INFOBOXPOSX = 1/16
INFOBOXPOSY = 81/100

BTNWIDTH = 70
BTNHEIGHT = 40
CLOSELBL = "Close"
CLOSEX, CLOSEY = -100, 40    # negatieve x omdat de positie van rechts bepaald wordt.


class Display(Parchment):
    """
    ...
    """
    def __init__(self, engine, hero):
        super().__init__(engine)

        self.name = GameState.Shop

        self.create_title = self.largefont.render(CREATETITLE, True, FONTCOLOR).convert_alpha()
        self.pouch_title = self.largefont.render(POUCHTITLE, True, FONTCOLOR).convert_alpha()

        self.cur_hero = hero
        self._init_face()
        self._init_boxes()

        self.close_button = Button(
            BTNWIDTH, BTNHEIGHT, (self.background.get_width() + CLOSEX, CLOSEY), CLOSELBL, Keys.Exit.value,
            COLORKEY, FONTCOLOR)

        self.info_label = ""

    def _init_face(self):
        face_image = pygame.image.load(self.cur_hero.FAC).convert_alpha()
        self.background.blit(face_image, (self._set_x(FACEPOSX), self._set_y(FACEPOSY)))

        for index, line in enumerate(self.cur_hero.alc.welcome_text(self.cur_hero.NAM)):
            rline = self.smallfont.render(line, True, FONTCOLOR).convert_alpha()
            if index < LINESNEXTTOFACE:
                self.background.blit(rline,
                                     (self._set_x(FACEPOSX) + face_image.get_width() + EXTRAFACESIZEX,
                                      self._set_y(FACEPOSY) + EXTRAFACESIZEY + index * SMALLLINEHEIGHT))
            else:
                self.background.blit(rline,
                                     (self._set_x(FACEPOSX),
                                      self._set_y(FACEPOSY) + EXTRAFACESIZEY + index * SMALLLINEHEIGHT))

    def _init_boxes(self):
        self._init_createbox()
        self._init_pouchbox()
        self._init_infobox()

    def _init_createbox(self):
        width = self.screen.get_width() * CREATEBOXWIDTH
        height = self.screen.get_height() * CREATEBOXHEIGHT + EXTRAHEIGHT
        # zoek in de PouchItemDatabase naar de enum keys die eindigen op _pot of _flk en stop die allemaal in een list.
        # en zoek ook naar potions die juiste alc skill waarde hebben om gemaakt te kunnen worden.
        self.createbox = CreateBox(self._set_x(CREATEBOXPOSX), self._set_y(CREATEBOXPOSY), int(width), int(height),
                                   [itm for itm in PouchItemDatabase
                                    if itm.name[-4:] in ('_pot', '_flk') and
                                    self.cur_hero.alc.tot >= itm.value['alc']], self.cur_hero.alc)

    def _init_pouchbox(self):
        width = self.screen.get_width() * POUCHBOXWIDTH
        height = self.screen.get_height() * POUCHBOXHEIGHT + EXTRAHEIGHT
        self.pouchbox = PouchBox(self._set_x(POUCHBOXPOSX), self._set_y(POUCHBOXPOSY), int(width), int(height),
                                 self.engine.data.pouch)

    def _init_infobox(self):
        width = self.screen.get_width() * INFOBOXWIDTH
        height = self.screen.get_height() * INFOBOXHEIGHT
        self.infobox = TextBox((self._set_x(INFOBOXPOSX), self._set_y(INFOBOXPOSY)), int(width), int(height))

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.MOUSEMOTION:
            self.info_label = ""
            self.createbox.cur_item = None
            self.pouchbox.cur_item = None

            if self.createbox.rect.collidepoint(event.pos):
                selected_name, self.info_label = self.createbox.mouse_hover(event)
                self.pouchbox.duplicate_selection(selected_name)
            if self.pouchbox.rect.collidepoint(event.pos):
                selected_name, self.info_label = self.pouchbox.mouse_hover(event)
                self.createbox.duplicate_selection(selected_name)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == Keys.Leftclick.value:
                if self.close_button.single_click(event) == Keys.Exit.value:
                    self._close()
                if self._handle_create_box_click(event):
                    return

            elif event.button in (Keys.Scrollup.value, Keys.Scrolldown.value):
                if self.createbox.rect.collidepoint(event.pos):
                    self.createbox.mouse_scroll(event)
                if self.pouchbox.rect.collidepoint(event.pos):
                    self.pouchbox.mouse_scroll(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == Keys.Exit.value:
                self._close()

    def render(self):
        """
        Teken alles op het scherm.
        """
        self.screen.fill(BACKGROUNDCOLOR)
        self.screen.blit(self.background, (0, 0))

        alc_title = self.largefont.render(self.cur_hero.alc.NAM, True, FONTCOLOR).convert_alpha()
        self.screen.blit(alc_title, (self._set_x(TITLEPOSX), self._set_y(TITLEPOSY)))

        self.screen.blit(self.create_title, ((self._set_x(CREATEBOXPOSX)) +
                                             (self.screen.get_width() * CREATEBOXWIDTH / 2) -
                                             (self.create_title.get_width() / 2),
                                             self._set_y(TITLEPOSY)))
        self.screen.blit(self.pouch_title, ((self._set_x(POUCHBOXPOSX)) +
                                            (self.screen.get_width() * POUCHBOXWIDTH / 2) -
                                            (self.pouch_title.get_width() / 2),
                                            self._set_y(TITLEPOSY)))

        sta_title = self.middlefont.render(
                    STATITLE.format(self.cur_hero.NAM) + str(self.cur_hero.sta.cur), True, FONTCOLOR).convert_alpha()
        self.screen.blit(sta_title, (self._set_x(STATITLEPOSX), self._set_y(STATITLEPOSY)))

        self.infobox.render(self.screen, self.info_label)
        self.createbox.render(self.screen)
        self.pouchbox.render(self.screen)
        self.close_button.render(self.screen, FONTCOLOR)

    def _handle_create_box_click(self, event):
        create_click, selected_potion = self.createbox.mouse_click(event)
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
