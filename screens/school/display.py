
"""
class: Display
"""

import pygame

from components import Button
from components import Transition
from constants import GameState
from constants import Keys
from database import SchoolDatabase

from screens.shop.infobox import InfoBox
from .learnedbox import LearnedBox
from .teachbox import TeachBox
from .selector import Selector


BACKGROUNDCOLOR = pygame.Color("black")
BACKGROUNDSPRITE = 'resources/sprites/parchment.png'
COLORKEY = pygame.Color("white")

FACEPOSX = 1/16
FACEPOSY = 3/16

FONTCOLOR = pygame.Color("black")
FONT = 'colonna'
LARGEFONTSIZE = 100
NORMALFONTSIZE = 50
SMALLFONTSIZE = 20

SMALLLINEHEIGHT = 30
EXTRAFACESIZE = 20
LINESNEXTTOFACE = 3

LEARNEDBOXWIDTH = 1/6      # van het scherm
LEARNEDBOXHEIGHT = 24/32
LEARNEDBOXPOSX = 2/5       # x op 2/5 van het scherm
LEARNEDBOXPOSY = 6/32

TEACHBOXWIDTH = 1/3
TEACHBOXHEIGHT = 24/32
TEACHBOXPOSX = 5/8
TEACHBOXPOSY = 6/32

EXTRAHEIGHT = 0         # zodat de laatste item er voor helft op komt

INFOBOXWIDTH = 8/32
INFOBOXHEIGHT = 7/32
INFOBOXPOSX = 2/32
INFOBOXPOSY = 23/32

SELECTORPOSX = 2/32
SELECTORPOSY = 20/32
SELECTORWIDTH = 31

BTNWIDTH = 70
BTNHEIGHT = 40
CLOSELBL = "Close"
CLOSEX, CLOSEY = -100, 40    # negatieve x omdat de positie van rechts bepaald wordt.


class Display:
    """
    ...
    """
    def __init__(self, engine, schooltype_list, face):
        self.engine = engine

        self.schooltype_list = schooltype_list

        self.selected_hero = self.engine.data.party['alagos']  # todo, alagos moet eigenlijk niet hard coded zijn

        self.screen = pygame.display.get_surface()
        self.name = GameState.Shop
        self.background = pygame.image.load(BACKGROUNDSPRITE).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)
        self.smallfont = pygame.font.SysFont(FONT, SMALLFONTSIZE)

        self._init_selectors()
        self._init_face(face)
        self._init_boxes()

        self.close_button = Button(
            BTNWIDTH, BTNHEIGHT, (self.background.get_width() + CLOSEX, CLOSEY), CLOSELBL, Keys.Exit.value,
            COLORKEY, FONTCOLOR)

        self.info_label = ""

    def _init_selectors(self):

        self.selectors = pygame.sprite.Group()

        for index, hero in enumerate(self.engine.data.party.values()):
            self.selectors.add(Selector(self._set_x(SELECTORPOSX) + index * SELECTORWIDTH,
                                        self._set_y(SELECTORPOSY), hero))

        self.selectors.draw(self.background)

    def _init_face(self, face):
        face_image = pygame.image.load(face).convert_alpha()
        self.background.blit(face_image, (self._set_x(FACEPOSX), self._set_y(FACEPOSY)))

        for index, line in enumerate(SchoolDatabase.welcome_text()):
            rline = self.smallfont.render(line, True, FONTCOLOR).convert_alpha()
            if index < LINESNEXTTOFACE:
                self.background.blit(rline,
                                     (self._set_x(FACEPOSX) + face_image.get_width() + EXTRAFACESIZE,
                                      self._set_y(FACEPOSY) + EXTRAFACESIZE + index * SMALLLINEHEIGHT))
            else:
                self.background.blit(rline,
                                     (self._set_x(FACEPOSX),
                                      self._set_y(FACEPOSY) + EXTRAFACESIZE + index * SMALLLINEHEIGHT))

    def _init_boxes(self):
        self._init_learnedbox()
        self._init_teachbox()
        self._init_infobox()

    def _init_learnedbox(self):
        width = self.screen.get_width() * LEARNEDBOXWIDTH
        height = self.screen.get_height() * LEARNEDBOXHEIGHT + EXTRAHEIGHT
        self.learnedbox = LearnedBox(self._set_x(LEARNEDBOXPOSX), self._set_y(LEARNEDBOXPOSY), int(width), int(height),
                                     self.selected_hero)

    def _init_teachbox(self):
        width = self.screen.get_width() * TEACHBOXWIDTH
        height = self.screen.get_height() * TEACHBOXHEIGHT + EXTRAHEIGHT
        self.teachbox = TeachBox(self._set_x(TEACHBOXPOSX), self._set_y(TEACHBOXPOSY), int(width), int(height),
                                 self.schooltype_list)

    def _init_infobox(self):
        width = self.screen.get_width() * INFOBOXWIDTH
        height = self.screen.get_height() * INFOBOXHEIGHT
        self.infobox = InfoBox(self._set_x(INFOBOXPOSX), self._set_y(INFOBOXPOSY), int(width), int(height))

    def on_enter(self):
        """
        Wanneer deze state op de stack komt, voer dit uit.
        """
        pass

    def on_exit(self):
        """
        Wanneer deze state onder een andere state van de stack komt, voer dit uit.
        Op dit moment nog niets echts.
        """
        pass

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """

        if event.type == pygame.MOUSEMOTION:

            self.info_label = ""
            self.learnedbox.cur_item = None

            if self.learnedbox.rect.collidepoint(event.pos):
                self.info_label = self.learnedbox.mouse_hover(event)
            if self.teachbox.rect.collidepoint(event.pos):
                self.info_label = self.teachbox.mouse_hover(event)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == Keys.Leftclick.value:

                if self.close_button.single_click(event) == Keys.Exit.value:
                    self._close()

                for selector in self.selectors:
                    hero = selector.mouse_click(event)
                    if hero:
                        self.selected_hero = hero
                        self._init_boxes()
                        break

            elif event.button in (Keys.Scrollup.value, Keys.Scrolldown.value):
                if self.learnedbox.rect.collidepoint(event.pos):
                    self.learnedbox.mouse_scroll(event)
                if self.teachbox.rect.collidepoint(event.pos):
                    self.teachbox.mouse_scroll(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == Keys.Exit.value:
                self._close()

    def multi_input(self, key_input, mouse_pos, dt):
        """
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
        Teken alles op het scherm, de titels, de boxen.
        """
        self.screen.fill(BACKGROUNDCOLOR)
        self.screen.blit(self.background, (0, 0))

        self.infobox.render(self.screen, self.info_label)
        self.learnedbox.render(self.screen)
        self.teachbox.render(self.screen)
        self.close_button.render(self.screen, FONTCOLOR, True)

    def _set_x(self, posx):
        return self.screen.get_width() * posx

    def _set_y(self, posy):
        return self.screen.get_height() * posy

    def _close(self):
        self.engine.gamestate.pop()
        self.engine.gamestate.push(Transition(self.engine.gamestate))
