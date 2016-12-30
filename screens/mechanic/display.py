
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
from constants import WeaponType as WeTy

from .upgradeablebox import UpgradeableBox
from screens.shop.selector import Selector

BACKGROUNDCOLOR = pygame.Color("black")
COLORKEY = pygame.Color("white")
FONTCOLOR = pygame.Color("black")

INFOBOXWIDTH = 25/100
INFOBOXHEIGHT = 11/100
INFOBOXPOSX = 1/16
INFOBOXPOSY = 81/100

BTNWIDTH = 70
BTNHEIGHT = 40
CLOSELBL = "Close"
CLOSEX, CLOSEY = -100, 40    # negatieve x omdat de positie van rechts bepaald wordt.

EXTRAHEIGHT = 0         # zodat de laatste item er voor helft op komt

UPGBOXWIDTH = 5/16
UPGBOXHEIGHT = 73/100
UPGBOXPOSX = 15/24
UPGBOXPOSY = 6/32

SELECTORPOSX = 2/32
SELECTORPOSY = 20/32
SELECTORWIDTH = 36

UPGRADELIST = [WeTy.swd, WeTy.haf, WeTy.pol, WeTy.mis, WeTy.thr,
               EqTy.sld, EqTy.hlm, EqTy.arm, EqTy.glv, EqTy.bts]


class Display(Parchment):
    """
    ...
    """
    def __init__(self, engine, hero):
        super().__init__(engine)

        self.eqptype = UPGRADELIST[0]

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

        for index, eqp_type in enumerate(UPGRADELIST):
            self.selectors.add(Selector(self._set_x(SELECTORPOSX) + index * SELECTORWIDTH,
                                        self._set_y(SELECTORPOSY), eqp_type))

        self.selectors.draw(self.background)

    def _init_boxes(self):
        self._init_infobox()
        self._init_upgradeablebox()

    def _init_infobox(self):
        width = self.screen.get_width() * INFOBOXWIDTH
        height = self.screen.get_height() * INFOBOXHEIGHT
        self.infobox = TextBox((self._set_x(INFOBOXPOSX), self._set_y(INFOBOXPOSY)), int(width), int(height))

    def _init_upgradeablebox(self):
        width = self.screen.get_width() * UPGBOXWIDTH
        height = self.screen.get_height() * UPGBOXHEIGHT + EXTRAHEIGHT
        self.upgbox = UpgradeableBox(self._set_x(UPGBOXPOSX), self._set_y(UPGBOXPOSY), int(width), int(height),
                                     self.eqptype, self.engine.data.party, self.engine.data.inventory)

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.MOUSEMOTION:
            self.info_label = ""

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == Keys.Leftclick.value:
                if self.close_button.single_click(event) == Keys.Exit.value:
                    self._close()

        elif event.type == pygame.KEYDOWN:
            if event.key == Keys.Exit.value:
                self._close()

    def render(self):
        """
        Teken alles op het scherm.
        """
        self.screen.fill(BACKGROUNDCOLOR)
        self.screen.blit(self.background, (0, 0))

        self.selectors.draw(self.background)

        self.infobox.render(self.screen, self.info_label)
        self.upgbox.render(self.screen)
        self.close_button.render(self.screen, FONTCOLOR)
