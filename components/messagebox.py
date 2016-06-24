
"""
class: MessageBox
"""

import pygame

from .screencapture import ScreenCapture
import keys
from statemachine import GameState

BACKGROUNDCOLOR = pygame.Color("black")

FONT = None
FONTSIZE = 30
FONTCOLOR = pygame.Color("black")
FONTPOSX = 40
FONTPOSY = 40
LINEHEIGHT = 25
IMGPOSX, IMGPOSY = 35, 60
FACEPOSX, FACEPOSY = 30, 42

MESSAGESPRITE = 'resources/sprites/parchment.png'


# noinspection PyMissingOrEmptyDocstring
class MessageBox(object):
    """
    Geeft een bericht weer op het scherm.
    """
    def __init__(self, gamestate, raw_text, face_image=None, spr_image=None, scr_capt=None):
        """
        :param spr_image: list van loaded images
        """
        self.gamestate = gamestate
        self.screen = pygame.display.get_surface()
        self.name = GameState.MessageBox

        if scr_capt is None:
            self.scr_capt = ScreenCapture()
        else:
            self.scr_capt = scr_capt

        self.font = pygame.font.SysFont(FONT, FONTSIZE)
        self.raw_text = raw_text
        self.vis_text = []
        self.face_image = face_image
        self.face_image_space = 0
        self.spr_image = spr_image
        self.spr_img_space = 0
        if self.face_image:
            self.face_image = pygame.image.load(face_image).convert_alpha()
            self.face_image_space = self.face_image.get_width()
        if self.spr_image:
            self.spr_img_space = self.spr_image[0].get_width()  # de breedte van de eerste uit de list

        text_widths = []
        for row in raw_text:
            self.vis_text.append(self.font.render(row, True, FONTCOLOR).convert_alpha())
            text_widths.append(self.font.render(row, True, FONTCOLOR).get_width())
        box_width = max(text_widths) + FONTPOSX * 2 + self.face_image_space + self.spr_img_space
        box_height = len(self.vis_text) * LINEHEIGHT + FONTPOSY * 2
        if box_height < self.face_image_space + FACEPOSY * 2:
            box_height = self.face_image_space + FACEPOSY * 2

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

        if self.face_image:
            self.surface.blit(self.face_image, (FACEPOSX, FACEPOSY))

        if self.spr_image:
            for i, line in enumerate(self.spr_image):
                self.surface.blit(line, (IMGPOSX, IMGPOSY + i * LINEHEIGHT))

        for i, line in enumerate(self.vis_text):
            if i == 0:
                self.surface.blit(line, (FONTPOSX + self.face_image_space,
                                         FONTPOSY + i * LINEHEIGHT))
            else:
                self.surface.blit(line, (FONTPOSX + self.face_image_space + self.spr_img_space,
                                         FONTPOSY + i * LINEHEIGHT))

        self.screen.blit(self.surface, self.rect.topleft)

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def multi_input(self, key_input, mouse_pos, dt):
        pass

    def update(self, dt):
        pass
