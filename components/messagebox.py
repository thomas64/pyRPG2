
"""
class: MessageBox
"""

import pygame

import components
import keys
import statemachine

BACKGROUNDCOLOR = pygame.Color("black")

FONT = None
FONTSIZE = 30
FONTCOLOR = pygame.Color("black")
FONTPOSX = 40
FONTPOSY = 40
LINEHEIGHT = 25
IMGPOSX = 35
IMGPOSY = 60
IMGSPACE = 30

MESSAGESPRITE = 'resources/sprites/parchment.png'


# noinspection PyMissingOrEmptyDocstring
class MessageBox(object):
    """
    Geeft een bericht weer op het scherm.
    """
    def __init__(self, gamestate, raw_text, image=None, scr_capt=None):
        self.gamestate = gamestate
        self.screen = pygame.display.get_surface()
        self.name = statemachine.States.MessageBox

        if scr_capt is None:
            self.scr_capt = components.ScreenCapture()
        else:
            self.scr_capt = scr_capt

        self.font = pygame.font.SysFont(FONT, FONTSIZE)
        self.raw_text = raw_text
        self.vis_text = []
        self.image = image
        self.img_space = 0
        if self.image:
            self.img_space = IMGSPACE

        text_widths = []
        for row in raw_text:
            self.vis_text.append(self.font.render(row, True, FONTCOLOR).convert_alpha())
            text_widths.append(self.font.render(row, True, FONTCOLOR).get_width())
        box_width = max(text_widths) + FONTPOSX * 2 + self.img_space
        box_height = len(self.vis_text) * LINEHEIGHT + FONTPOSY * 2

        self.surface = pygame.Surface((box_width, box_height))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)

        self.surface.fill(BACKGROUNDCOLOR)
        self.surface.set_colorkey(BACKGROUNDCOLOR)

        self.background = pygame.image.load(MESSAGESPRITE).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.surface.get_size())

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.KEYDOWN:
            if event.key == keys.EXIT:
                self.gamestate.pop()
            elif event.key in keys.SELECT:
                self.gamestate.pop()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == keys.LEFTCLICK:
                self.gamestate.pop()

    def render(self):
        """
        Teken de tekst.
        """
        self.scr_capt.render()

        self.surface.blit(self.background, (0, 0))

        if self.image:
            for i, line in enumerate(self.image):
                self.surface.blit(line, (IMGPOSX, IMGPOSY + i * LINEHEIGHT))

        for i, line in enumerate(self.vis_text):
            if i == 0:
                self.surface.blit(line, (FONTPOSX, FONTPOSY + i * LINEHEIGHT))
            else:
                self.surface.blit(line, (FONTPOSX + self.img_space, FONTPOSY + i * LINEHEIGHT))

        self.screen.blit(self.surface, self.rect.topleft)

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def multi_input(self, key_input, mouse_pos, dt):
        pass

    def update(self, dt):
        pass
