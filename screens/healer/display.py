
"""
class: Display
"""

import pygame

from components import Button
from components import MessageBox
from components import Parchment

from constants import GameState
from constants import Keys
from constants import SFX

COLORKEY = pygame.Color("white")
FONTCOLOR = pygame.Color("black")

LEFTBOXTITLE = "Left"
RIGHTBOXTITLE = "Right"
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
STATITLEPOSY = 70/100

INFOBOXWIDTH = 30/100
INFOBOXHEIGHT = 16/100
INFOBOXPOSX = 1/16
INFOBOXPOSY = 76/100

BTNWIDTH = 70
BTNHEIGHT = 40
CLOSELBL = "Close"
CLOSEX, CLOSEY = -100, 40    # negatieve x omdat de positie van rechts bepaald wordt.

EXTRAHEIGHT = 0         # zodat de laatste item er voor helft op komt

LEFTBOXWIDTH = 20 / 100
LEFTBOXHEIGHT = 73 / 100
LEFTBOXPOSX = 40 / 100
LEFTBOXPOSY = 6 / 32

RIGHTBOXWIDTH = 26/100
RIGHTBOXHEIGHT = 73/100
RIGHTBOXPOSX = 64/100
RIGHTBOXPOSY = 6/32

SELECTORPOSX = 2/32
SELECTORPOSY = 65/100
SELECTORWIDTH = 36


class Display(Parchment):
    """
    ...
    """
    def __init__(self, engine, hero, party):
        super().__init__(engine)

        self.name = GameState.Shop

        self.left_box_title = self.largefont.render(LEFTBOXTITLE, True, FONTCOLOR).convert_alpha()
        self.right_box_title = self.largefont.render(RIGHTBOXTITLE, True, FONTCOLOR).convert_alpha()

        self.cur_hero = hero
        self.party = party
        # self._init_selectors()
        # self._init_face()
        self._init_boxes()

        self.close_button = Button(
            BTNWIDTH, BTNHEIGHT, (self.background.get_width() + CLOSEX, CLOSEY), CLOSELBL, Keys.Exit.value,
            COLORKEY, FONTCOLOR)

    def _init_boxes(self):
        self._init_infobox(INFOBOXWIDTH, INFOBOXHEIGHT, INFOBOXPOSX, INFOBOXPOSY)

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

            elif event.button in (Keys.Scrollup.value, Keys.Scrolldown.value):
                pass

        elif event.type == pygame.KEYDOWN:
            if event.key == Keys.Exit.value:
                self._close()

    def render(self):
        """
        Teken alles op het scherm.
        """
        super().render()

        hlr_title = self.largefont.render(self.cur_hero.hlr.NAM, True, FONTCOLOR).convert_alpha()
        self.screen.blit(hlr_title, (self._set_x(TITLEPOSX), self._set_y(TITLEPOSY)))

        self.screen.blit(self.left_box_title, ((self._set_x(LEFTBOXPOSX)) +
                                               (self.screen.get_width() * LEFTBOXWIDTH / 2) -
                                               (self.left_box_title.get_width() / 2),
                                               self._set_y(TITLEPOSY)))
        self.screen.blit(self.right_box_title, ((self._set_x(RIGHTBOXPOSX)) +
                                                (self.screen.get_width() * RIGHTBOXWIDTH / 2) -
                                                (self.right_box_title.get_width() / 2),
                                                self._set_y(TITLEPOSY)))

        sta_title = self.middlefont.render(
                    STATITLE.format(self.cur_hero.NAM) + str(self.cur_hero.sta.cur), True, FONTCOLOR).convert_alpha()
        self.screen.blit(sta_title, (self._set_x(STATITLEPOSX), self._set_y(STATITLEPOSY)))

        self.close_button.render(self.screen, FONTCOLOR)
