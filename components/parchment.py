
"""
class: Parchment
"""

import pygame

from constants import Keys
from constants import SFX

from .sprites import Button
from .textbox import TextBox
from .transition import Transition


COLORKEY = pygame.Color("white")
FONTCOLOR = pygame.Color("black")
BACKGROUNDCOLOR = pygame.Color("black")
BACKGROUNDSPRITE = 'resources/sprites/parchment.png'

FONT = 'colonna'
SUBFONT = 'verdana'
LARGEFONTSIZE = 100
NORMALFONTSIZE = 50
MIDDLEFONTSIZE = 40
SMALLFONTSIZE = 20
TINYFONTSIZE = 12


class Parchment(object):
    """
    ...
    """
    def __init__(self, engine, left_title, right_title):
        self.engine = engine

        self.screen = pygame.display.get_surface()
        self.background = pygame.image.load(BACKGROUNDSPRITE).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())

        self.fontcolor = FONTCOLOR

        self.largefont = pygame.font.SysFont(FONT, LARGEFONTSIZE)
        self.normalfont = pygame.font.SysFont(FONT, NORMALFONTSIZE)
        self.middlefont = pygame.font.SysFont(FONT, MIDDLEFONTSIZE)
        self.smallfont = pygame.font.SysFont(FONT, SMALLFONTSIZE)
        self.tinyfont = pygame.font.SysFont(SUBFONT, TINYFONTSIZE)

        self.info_label = ""
        self.selectors = pygame.sprite.Group()
        self.subtype_list = list()
        self.subtype = None

        self.main_title = ""
        self.main_title_pos_x = 0
        self.main_title_pos_y = 0
        self.source_title1 = ""
        self.source_title1_pos_x = 0
        self.source_title1_pos_y = 0
        self.source_title2 = ""
        self.source_title2_pos_x = 0
        self.source_title2_pos_y = 0
        self.sub_title_pos_x = 0
        self.sub_title_pos_y1 = 0
        self.sub_title_pos_y2 = 0

        self.face_pos_x = 0
        self.face_pos_y = 0
        self.extra_face_size_x = 0
        self.extra_face_size_y = 0
        self.lines_next_to_face = 0
        self.small_line_height = 0

        self.leftbox = None
        self.rightbox = None
        self.leftbox_title = self.largefont.render(left_title, True, FONTCOLOR).convert_alpha()
        self.rightbox_title = self.largefont.render(right_title, True, FONTCOLOR).convert_alpha()
        self.leftbox_width = 0
        self.leftbox_height = 0
        self.leftbox_pos_x = 0
        self.leftbox_pos_y = 0
        self.rightbox_width = 0
        self.rightbox_height = 0
        self.rightbox_pos_x = 0
        self.rightbox_pos_y = 0
        self.infobox_width = 0
        self.infobox_height = 0
        self.infobox_pos_x = 0
        self.infobox_pos_y = 0

        self.closebutton_width = 60
        self.closebutton_height = 40
        self.closebutton_label = "Close"
        self.closebutton_pos_x = -80  # negatieve x omdat de positie van rechts bepaald wordt.
        self.closebutton_pos_y = 30

    def _init_face_and_text(self, face, text):
        face_image = pygame.image.load(face).convert_alpha()
        self.background.blit(face_image, (self._set_x(self.face_pos_x), self._set_y(self.face_pos_y)))

        for index, line in enumerate(text):
            rline = self.smallfont.render(line, True, FONTCOLOR).convert_alpha()
            if index < self.lines_next_to_face:
                self.background.blit(
                    rline,
                    (self._set_x(self.face_pos_x) + face_image.get_width() + self.extra_face_size_x,
                     self._set_y(self.face_pos_y) + self.extra_face_size_y + index * self.small_line_height))
            else:
                self.background.blit(
                    rline,
                    (self._set_x(self.face_pos_x),
                     self._set_y(self.face_pos_y) + self.extra_face_size_y + index * self.small_line_height))

    def _init_boxes(self):
        pass

    def _init_infobox(self):
        width = self.screen.get_width() * self.infobox_width
        height = self.screen.get_height() * self.infobox_height
        self.infobox = TextBox((self._set_x(self.infobox_pos_x), self._set_y(self.infobox_pos_y)),
                               int(width), int(height))

    def _init_buttons(self):
        self.closebutton = Button(
            self.closebutton_width, self.closebutton_height,
            (self.background.get_width() + self.closebutton_pos_x, self.closebutton_pos_y),
            self.closebutton_label, Keys.Exit.value, COLORKEY, FONTCOLOR)

    # noinspection PyMissingOrEmptyDocstring
    def on_enter(self):
        pass

    # noinspection PyMissingOrEmptyDocstring
    def on_exit(self):
        pass

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """

        # todo, sellbox en buybox met toetsenbord
        # todo, equipment die hero's aanhebben kunnen sellen

        if event.type == pygame.MOUSEMOTION:
            self.info_label = ""
            self.leftbox.cur_item = None
            self.rightbox.cur_item = None

            if self.leftbox.rect.collidepoint(event.pos):
                selected_name, self.info_label = self.leftbox.mouse_hover(event)
                self.rightbox.duplicate_selection(selected_name)
            if self.rightbox.rect.collidepoint(event.pos):
                selected_name, self.info_label = self.rightbox.mouse_hover(event)
                self.leftbox.duplicate_selection(selected_name)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == Keys.Leftclick.value:
                if self.closebutton.single_click(event) == Keys.Exit.value:
                    self._close()
                # return of anders worden sommigen variabelen weer overschreven.
                if self._handle_leftbox_click(event):
                    return
                if self._handle_rightbox_click(event):
                    return

                for selector in self.selectors:
                    if selector:
                        subtype = selector.mouse_click(event)
                        if subtype:
                            if subtype != self.subtype:
                                self.engine.audio.play_sound(SFX.menu_switch)
                                self.subtype = subtype
                                self._init_boxes()
                                break

            elif event.button in (Keys.Scrollup.value, Keys.Scrolldown.value):
                if self.leftbox.rect.collidepoint(event.pos):
                    self.leftbox.mouse_scroll(event)
                if self.rightbox.rect.collidepoint(event.pos):
                    self.rightbox.mouse_scroll(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == Keys.Exit.value:
                self._close()
            elif event.key == Keys.Prev.value:
                self._previous()
            elif event.key == Keys.Next.value:
                self._next()

    # noinspection PyMissingOrEmptyDocstring
    def multi_input(self, key_input, mouse_pos, dt):
        pass

    # noinspection PyMissingOrEmptyDocstring
    def update(self, dt):
        pass

    # noinspection PyMissingOrEmptyDocstring
    def render(self):
        self.screen.fill(BACKGROUNDCOLOR)
        self.screen.blit(self.background, (0, 0))

        main_title = self.largefont.render(self.main_title, True, FONTCOLOR).convert_alpha()
        self.screen.blit(main_title, (self._set_x(self.main_title_pos_x), self._set_y(self.main_title_pos_y)))
        source_title1 = self.middlefont.render(self.source_title1, True, FONTCOLOR).convert_alpha()
        self.screen.blit(source_title1, (self._set_x(self.source_title1_pos_x), self._set_y(self.source_title1_pos_y)))
        source_title2 = self.middlefont.render(self.source_title2, True, FONTCOLOR).convert_alpha()
        self.screen.blit(source_title2, (self._set_x(self.source_title2_pos_x), self._set_y(self.source_title2_pos_y)))

        # titels midden boven de boxen
        self.screen.blit(self.leftbox_title, ((self._set_x(self.leftbox_pos_x)) +
                                              (self.screen.get_width() * self.leftbox_width / 2) -
                                              (self.leftbox_title.get_width() / 2),
                                              self._set_y(self.main_title_pos_y)))
        self.screen.blit(self.rightbox_title, ((self._set_x(self.rightbox_pos_x)) +
                                               (self.screen.get_width() * self.rightbox_width / 2) -
                                               (self.rightbox_title.get_width() / 2),
                                               self._set_y(self.main_title_pos_y)))

        # subtitles boven de boxen
        xpos = self._set_x(self.leftbox_pos_x) + self.sub_title_pos_x
        for column in self.leftbox.total_columns:
            title1 = self.tinyfont.render(column[2], True, self.fontcolor).convert_alpha()
            title2 = self.tinyfont.render(column[3], True, self.fontcolor).convert_alpha()
            self.screen.blit(title1, (xpos + column[1], self._set_y(self.sub_title_pos_y1)))
            self.screen.blit(title2, (xpos + column[1], self._set_y(self.sub_title_pos_y2)))
        xpos = self._set_x(self.rightbox_pos_x) + self.sub_title_pos_x
        for column in self.rightbox.total_columns:
            title1 = self.tinyfont.render(column[2], True, self.fontcolor).convert_alpha()
            title2 = self.tinyfont.render(column[3], True, self.fontcolor).convert_alpha()
            self.screen.blit(title1, (xpos + column[1], self._set_y(self.sub_title_pos_y1)))
            self.screen.blit(title2, (xpos + column[1], self._set_y(self.sub_title_pos_y2)))

        if self.selectors:
            self.selectors.draw(self.background)

        self.infobox.render(self.screen, self.info_label)
        self.leftbox.render(self.screen)
        self.rightbox.render(self.screen)
        self.closebutton.render(self.screen, FONTCOLOR)

    def _handle_leftbox_click(self, event):
        pass

    def _handle_rightbox_click(self, event):
        pass

    def _set_x(self, posx):
        return self.screen.get_width() * posx

    def _set_y(self, posy):
        return self.screen.get_height() * posy

    def _close(self):
        self.engine.audio.play_sound(SFX.scroll)
        self.engine.gamestate.pop()
        self.engine.gamestate.push(Transition(self.engine.gamestate))

    def _previous(self):
        self.engine.audio.play_sound(SFX.menu_switch)
        for index, subtype in enumerate(self.subtype_list):
            if subtype == self.subtype:
                i = index - 1
                if i < 0:
                    i = len(self.subtype_list) - 1
                self.subtype = self.subtype_list[i]
                self._init_boxes()
                break

    def _next(self):
        self.engine.audio.play_sound(SFX.menu_switch)
        for index, subtype in enumerate(self.subtype_list):
            if subtype == self.subtype:
                i = index + 1
                if i >= len(self.subtype_list):
                    i = 0
                self.subtype = self.subtype_list[i]
                self._init_boxes()
                break
