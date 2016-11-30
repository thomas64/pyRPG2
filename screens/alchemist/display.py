
"""
class: Display
"""

import pygame

from components import Button
from components import Transition
from constants import GameState
from constants import Keys
from database import PouchItemDatabase

from screens.shop.infobox import InfoBox
from .createbox import CreateBox
from .pouchbox import PouchBox


BACKGROUNDCOLOR = pygame.Color("black")
BACKGROUNDSPRITE = 'resources/sprites/parchment.png'
COLORKEY = pygame.Color("white")
FONTCOLOR = pygame.Color("black")
FONT = 'colonna'
LARGEFONTSIZE = 100
NORMALFONTSIZE = 50
SMALLFONTSIZE = 20

CREATEBOXWIDTH = 3/16
CREATEBOXHEIGHT = 73/100
CREATEBOXPOSX = 2/5
CREATEBOXPOSY = 6/32

POUCHBOXWIDTH = 3/16     # van het scherm
POUCHBOXHEIGHT = 73/100
POUCHBOXPOSX = 16/24     # x op 16/24 van het scherm
POUCHBOXPOSY = 6/32

EXTRAHEIGHT = 0         # zodat de laatste item er voor helft op komt

CREATETITLE = "Create"
POUCHTITLE = "Pouch"
TITLEPOSY = 1/32

INFOBOXWIDTH = 1/4
INFOBOXHEIGHT = 1/6
INFOBOXPOSX = 1/16
INFOBOXPOSY = 6/8

BTNWIDTH = 70
BTNHEIGHT = 40
CLOSELBL = "Close"
CLOSEX, CLOSEY = -100, 40    # negatieve x omdat de positie van rechts bepaald wordt.


class Display(object):
    """
    ...
    """
    def __init__(self, engine):
        self.engine = engine

        self.screen = pygame.display.get_surface()
        self.name = GameState.Shop
        self.background = pygame.image.load(BACKGROUNDSPRITE).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)
        self.smallfont = pygame.font.SysFont(FONT, SMALLFONTSIZE)
        self.create_title = self.largefont.render(CREATETITLE, True, FONTCOLOR).convert_alpha()
        self.pouch_title = self.largefont.render(POUCHTITLE, True, FONTCOLOR).convert_alpha()

        self._init_boxes()

        self.close_button = Button(
            BTNWIDTH, BTNHEIGHT, (self.background.get_width() + CLOSEX, CLOSEY), CLOSELBL, Keys.Exit.value,
            COLORKEY, FONTCOLOR)

        self.info_label = ""

    def _init_boxes(self):
        self._init_createbox()
        self._init_pouchbox()
        self._init_infobox()

    def _init_createbox(self):
        width = self.screen.get_width() * CREATEBOXWIDTH
        height = self.screen.get_height() * CREATEBOXHEIGHT + EXTRAHEIGHT
        # zoek in de PouchItemDatabase naar de enum keys die eindigen op _pot of _flk en stop die allemaal in een list.
        self.createbox = CreateBox(self._set_x(CREATEBOXPOSX), self._set_y(CREATEBOXPOSY), int(width), int(height),
                                   [itm for itm in PouchItemDatabase if itm.name[-4:] in ('_pot', '_flk')])

    def _init_pouchbox(self):
        width = self.screen.get_width() * POUCHBOXWIDTH
        height = self.screen.get_height() * POUCHBOXHEIGHT + EXTRAHEIGHT
        self.pouchbox = PouchBox(self._set_x(POUCHBOXPOSX), self._set_y(POUCHBOXPOSY), int(width), int(height),
                                 self.engine.data.pouch)

    def _init_infobox(self):
        width = self.screen.get_width() * INFOBOXWIDTH
        height = self.screen.get_height() * INFOBOXHEIGHT
        self.infobox = InfoBox(self._set_x(INFOBOXPOSX), self._set_y(INFOBOXPOSY), int(width), int(height))

    def on_enter(self):
        pass

    def on_exit(self):
        pass

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

            elif event.button in (Keys.Scrollup.value, Keys.Scrolldown.value):
                if self.createbox.rect.collidepoint(event.pos):
                    self.createbox.mouse_scroll(event)
                if self.pouchbox.rect.collidepoint(event.pos):
                    self.pouchbox.mouse_scroll(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == Keys.Exit.value:
                self._close()

    def multi_input(self, key_input, mouse_pos, dt):
        """
        ...
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    def update(self, dt):
        """
        ...
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    def render(self):
        """
        Teken alles op het scherm.
        """
        self.screen.fill(BACKGROUNDCOLOR)
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.create_title, ((self._set_x(CREATEBOXPOSX)) +
                                             (self.screen.get_width() * CREATEBOXWIDTH / 2) -
                                             (self.create_title.get_width() / 2),
                                             self._set_y(TITLEPOSY)))
        self.screen.blit(self.pouch_title, ((self._set_x(POUCHBOXPOSX)) +
                                            (self.screen.get_width() * POUCHBOXWIDTH / 2) -
                                            (self.pouch_title.get_width() / 2),
                                            self._set_y(TITLEPOSY)))

        self.infobox.render(self.screen, self.info_label)
        self.createbox.render(self.screen)
        self.pouchbox.render(self.screen)
        self.close_button.render(self.screen, FONTCOLOR, True)

    def _set_x(self, posx):
        return self.screen.get_width() * posx

    def _set_y(self, posy):
        return self.screen.get_height() * posy

    def _close(self):
        self.engine.gamestate.pop()
        self.engine.gamestate.push(Transition(self.engine.gamestate))
