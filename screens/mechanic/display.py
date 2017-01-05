
"""
class: Display
"""

import random

import pygame

from components import Button
from components import Parchment
from components import TextBox

from constants import EquipmentType as EqTy
from constants import GameState
from constants import Keys
from constants import SFX

from .createbox import CreateBox
from .inventorybox import InventoryBox
from screens.shop.selector import Selector

BACKGROUNDCOLOR = pygame.Color("black")
COLORKEY = pygame.Color("white")
FONTCOLOR = pygame.Color("black")

INFOBOXWIDTH = 1/4
INFOBOXHEIGHT = 1/6
INFOBOXPOSX = 1/16
INFOBOXPOSY = 6/8

BTNWIDTH = 70
BTNHEIGHT = 40
CLOSELBL = "Close"
CLOSEX, CLOSEY = -100, 40    # negatieve x omdat de positie van rechts bepaald wordt.

EXTRAHEIGHT = 0         # zodat de laatste item er voor helft op komt

CREATEBOXWIDTH = 20 / 100
CREATEBOXHEIGHT = 73 / 100
CREATEBOXPOSX = 40 / 100
CREATEBOXPOSY = 6 / 32

INVENTORYBOXWIDTH = 26/100
INVENTORYBOXHEIGHT = 73/100
INVENTORYBOXPOSX = 64/100
INVENTORYBOXPOSY = 6/32

SELECTORPOSX = 2/32
SELECTORPOSY = 20/32
SELECTORWIDTH = 36

CREATELIST = [EqTy.wpn, EqTy.sld, EqTy.hlm, EqTy.arm, EqTy.clk, EqTy.glv, EqTy.blt, EqTy.bts]


class Display(Parchment):
    """
    ...
    """
    def __init__(self, engine, hero):
        super().__init__(engine)

        self.eqptype = CREATELIST[0]

        self.name = GameState.Shop

        # self.create_title = self.largefont.render(CREATETITLE, True, FONTCOLOR).convert_alpha()
        # self.pouch_title = self.largefont.render(POUCHTITLE, True, FONTCOLOR).convert_alpha()

        self.cur_hero = hero
        self._init_selectors()
        # self._init_face()
        self._init_boxes()

        self.close_button = Button(
            BTNWIDTH, BTNHEIGHT, (self.background.get_width() + CLOSEX, CLOSEY), CLOSELBL, Keys.Exit.value,
            COLORKEY, FONTCOLOR)

        self.info_label = ""

    def _init_selectors(self):
        self.selectors = pygame.sprite.Group()

        for index, eqp_type in enumerate(CREATELIST):
            self.selectors.add(Selector(self._set_x(SELECTORPOSX) + index * SELECTORWIDTH,
                                        self._set_y(SELECTORPOSY), eqp_type))

        self.selectors.draw(self.background)

    def _init_boxes(self):
        self._init_infobox()
        self._init_createbox()
        self._init_inventorybox()

    def _init_infobox(self):
        width = self.screen.get_width() * INFOBOXWIDTH
        height = self.screen.get_height() * INFOBOXHEIGHT
        self.infobox = TextBox((self._set_x(INFOBOXPOSX), self._set_y(INFOBOXPOSY)), int(width), int(height))

    def _init_createbox(self):
        width = self.screen.get_width() * CREATEBOXWIDTH
        height = self.screen.get_height() * CREATEBOXHEIGHT + EXTRAHEIGHT

        if self.eqptype == EqTy.wpn:
            from database.weapon import WeaponDatabase as DataBase
        elif self.eqptype == EqTy.sld:
            from database.shield import ShieldDatabase as DataBase
        elif self.eqptype == EqTy.hlm:
            from database.helmet import HelmetDatabase as DataBase
        elif self.eqptype == EqTy.arm:
            from database.armor import ArmorDatabase as DataBase
        elif self.eqptype == EqTy.clk:
            from database.cloak import CloakDatabase as DataBase
        elif self.eqptype == EqTy.glv:
            from database.gloves import GlovesDatabase as DataBase
        elif self.eqptype == EqTy.blt:
            from database.belt import BeltDatabase as DataBase
        elif self.eqptype == EqTy.bts:
            from database.boots import BootsDatabase as DataBase
        else:
            raise AttributeError

        self.createbox = CreateBox(self._set_x(CREATEBOXPOSX), self._set_y(CREATEBOXPOSY), int(width), int(height),
                                   DataBase)

    def _init_inventorybox(self):
        width = self.screen.get_width() * INVENTORYBOXWIDTH
        height = self.screen.get_height() * INVENTORYBOXHEIGHT + EXTRAHEIGHT
        self.inventorybox = InventoryBox(self._set_x(INVENTORYBOXPOSX), self._set_y(INVENTORYBOXPOSY),
                                         int(width), int(height),
                                         self.eqptype, self.engine.data.party,
                                         self.engine.data.pouch, self.engine.data.inventory)

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.MOUSEMOTION:
            self.info_label = ""
            self.createbox.cur_item = None
            self.inventorybox.cur_item = None

            if self.createbox.rect.collidepoint(event.pos):
                selected_name, self.info_label = self.createbox.mouse_hover(event)
            if self.inventorybox.rect.collidepoint(event.pos):
                selected_name, self.info_label = self.inventorybox.mouse_hover(event)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == Keys.Leftclick.value:

                if self.close_button.single_click(event) == Keys.Exit.value:
                    self._close()

                for selector in self.selectors:
                    eqptype = selector.mouse_click(event)
                    if eqptype:
                        if eqptype != self.eqptype:
                            self.engine.audio.play_sound(SFX.menu_switch)
                            self.eqptype = eqptype
                            self._init_boxes()
                            break

            elif event.button in (Keys.Scrollup.value, Keys.Scrolldown.value):
                if self.createbox.rect.collidepoint(event.pos):
                    self.createbox.mouse_scroll(event)
                if self.inventorybox.rect.collidepoint(event.pos):
                    self.inventorybox.mouse_scroll(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == Keys.Exit.value:
                self._close()
            elif event.key == Keys.Prev.value:
                self._previous()
            elif event.key == Keys.Next.value:
                self._next()

    def update(self, dt):
        """
        Update de selector border color.
        Update de gold quantity.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        for selector in self.selectors:
            selector.update(self.eqptype)

    def render(self):
        """
        Teken alles op het scherm.
        """
        self.screen.fill(BACKGROUNDCOLOR)
        self.screen.blit(self.background, (0, 0))

        self.selectors.draw(self.background)

        self.infobox.render(self.screen, self.info_label)
        self.createbox.render(self.screen)
        self.inventorybox.render(self.screen)
        self.close_button.render(self.screen, FONTCOLOR)

    def _previous(self):
        self.engine.audio.play_sound(SFX.menu_switch)
        for index, eqptype in enumerate(CREATELIST):
            if eqptype == self.eqptype:
                i = index - 1
                if i < 0:
                    i = len(CREATELIST) - 1
                self.eqptype = CREATELIST[i]
                self._init_boxes()
                break

    def _next(self):
        self.engine.audio.play_sound(SFX.menu_switch)
        for index, eqptype in enumerate(CREATELIST):
            if eqptype == self.eqptype:
                i = index + 1
                if i >= len(CREATELIST):
                    i = 0
                self.eqptype = CREATELIST[i]
                self._init_boxes()
                break
