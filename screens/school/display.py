
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
from .knownbox import KnownBox
from .learnbox import LearnBox
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
MIDDLEFONTSIZE = 40
SMALLFONTSIZE = 20

SMALLLINEHEIGHT = 30
EXTRAFACESIZE = 20
LINESNEXTTOFACE = 3

KNOWNBOXWIDTH = 7/32    # van het scherm
KNOWNBOXHEIGHT = 24/32
KNOWNBOXPOSX = 2/5      # x op 2/5 van het scherm
KNOWNBOXPOSY = 6/32

LEARNBOXWIDTH = 9/32
LEARNBOXHEIGHT = 24/32
LEARNBOXPOSX = 21/32
LEARNBOXPOSY = 6/32

EXTRAHEIGHT = 0         # zodat de laatste item er voor helft op komt

LEARNTITLE = "Learn"
KNOWNTITLE = "Known"
GOLDTITLE = "Gold: "
XPTITLE = "XP Remaining: "
TITLEPOSY = 1/32

INFOBOXWIDTH = 8/32
INFOBOXHEIGHT = 7/32
INFOBOXPOSX = 2/32
INFOBOXPOSY = 23/32

SELECTORPOSX = 2/32
SELECTORPOSY = 18/32
SELECTORWIDTH = 31

GOLDTITLEPOSX = 1/16
GOLDTITLEPOSY = 39/64
XPTITLEPOSX = 1/16
XPTITLEPOSY = 42/64

HEROTITLEPOSX = 1/16

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
        self.middlefont = pygame.font.SysFont(FONT, MIDDLEFONTSIZE)
        self.smallfont = pygame.font.SysFont(FONT, SMALLFONTSIZE)
        self.learn_title = self.largefont.render(LEARNTITLE, True, FONTCOLOR).convert_alpha()
        self.known_title = self.largefont.render(KNOWNTITLE, True, FONTCOLOR).convert_alpha()
        self.gold_amount = None
        self.xp_amount = None

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
        self._init_knownbox()
        self._init_learnbox()
        self._init_infobox()

    def _init_knownbox(self):
        width = self.screen.get_width() * KNOWNBOXWIDTH
        height = self.screen.get_height() * KNOWNBOXHEIGHT + EXTRAHEIGHT
        self.knownbox = KnownBox(self._set_x(KNOWNBOXPOSX), self._set_y(KNOWNBOXPOSY), int(width), int(height),
                                 self.selected_hero)

    def _init_learnbox(self):
        width = self.screen.get_width() * LEARNBOXWIDTH
        height = self.screen.get_height() * LEARNBOXHEIGHT + EXTRAHEIGHT
        self.learnbox = LearnBox(self._set_x(LEARNBOXPOSX), self._set_y(LEARNBOXPOSY), int(width), int(height),
                                 self.schooltype_list, self.selected_hero)

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
            self.knownbox.cur_item = None
            self.learnbox.cur_item = None

            if self.knownbox.rect.collidepoint(event.pos):
                self.info_label = self.knownbox.mouse_hover(event)
            if self.learnbox.rect.collidepoint(event.pos):
                self.info_label = self.learnbox.mouse_hover(event)

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
                if self.knownbox.rect.collidepoint(event.pos):
                    self.knownbox.mouse_scroll(event)
                if self.learnbox.rect.collidepoint(event.pos):
                    self.learnbox.mouse_scroll(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == Keys.Exit.value:
                self._close()
            elif event.key == Keys.Prev.value:
                self._previous()
            elif event.key == Keys.Next.value:
                self._next()

    def multi_input(self, key_input, mouse_pos, dt):
        """
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    def update(self, dt):
        """
        Update de gold quantity.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        self.gold_amount = self.engine.data.pouch['gold'].qty
        self.xp_amount = self.selected_hero.exp.rem

    def render(self):
        """
        Teken alles op het scherm, de titels, de boxen.
        """
        self.screen.fill(BACKGROUNDCOLOR)
        self.screen.blit(self.background, (0, 0))
        # titels midden boven de boxen
        self.screen.blit(self.learn_title, ((self._set_x(LEARNBOXPOSX)) +
                                            (self.screen.get_width() * LEARNBOXWIDTH / 2) -
                                            (self.learn_title.get_width() / 2),
                                            self._set_y(TITLEPOSY)))
        self.screen.blit(self.known_title, ((self._set_x(KNOWNBOXPOSX)) +
                                            (self.screen.get_width() * KNOWNBOXWIDTH / 2) -
                                            (self.known_title.get_width() / 2),
                                            self._set_y(TITLEPOSY)))

        hero_title = self.largefont.render(self.selected_hero.NAM, True, FONTCOLOR).convert_alpha()
        self.screen.blit(hero_title, (self._set_x(HEROTITLEPOSX), self._set_y(TITLEPOSY)))
        gold_title = self.middlefont.render(GOLDTITLE + str(self.gold_amount), True, FONTCOLOR).convert_alpha()
        self.screen.blit(gold_title, (self._set_x(GOLDTITLEPOSX), self._set_y(GOLDTITLEPOSY)))
        xp_title = self.middlefont.render(XPTITLE + str(self.xp_amount), True, FONTCOLOR).convert_alpha()
        self.screen.blit(xp_title, (self._set_x(XPTITLEPOSX), self._set_y(XPTITLEPOSY)))

        self.infobox.render(self.screen, self.info_label)
        self.knownbox.render(self.screen)
        self.learnbox.render(self.screen)
        self.close_button.render(self.screen, FONTCOLOR, True)

    def _set_x(self, posx):
        return self.screen.get_width() * posx

    def _set_y(self, posy):
        return self.screen.get_height() * posy

    def _previous(self):
        party_list = list(self.engine.data.party.values())
        index = party_list.index(self.selected_hero)
        index -= 1
        if index < 0:
            index = len(party_list)-1
        self.selected_hero = party_list[index]
        self._init_boxes()

    def _next(self):
        party_list = list(self.engine.data.party.values())
        index = party_list.index(self.selected_hero)
        index += 1
        if index > len(party_list)-1:
            index = 0
        self.selected_hero = party_list[index]
        self._init_boxes()

    def _close(self):
        self.engine.gamestate.pop()
        self.engine.gamestate.push(Transition(self.engine.gamestate))
