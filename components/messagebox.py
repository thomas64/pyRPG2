
"""
class: MessageBox
class: LoadScreen
class: Animation
"""

import pygame

from constants import GameState
from constants import Keys
from constants import SFX

from .screencapture import ScreenCapture


BACKGROUNDCOLOR = pygame.Color("black")

FONT = None
FONTSIZE = 30
FONTCOLOR = pygame.Color("black")
FONTPOSX = 40
FONTPOSY = 40
LINEHEIGHT = 25
IMGPOSX, IMGPOSY = 35, 60
FACEPOSX, FACEPOSY = 30, 42
FULLPOSX = 45   # wanneer messagebox alleen een plaatje is.

MESSAGESPRITE = 'resources/sprites/parchment.png'


PATH = 'resources/sprites/heroes/01s_alagos.png'
TIME = 0.3
ICONX = 200
ICONY = 25
ICONW = 32


# noinspection PyMissingOrEmptyDocstring
class MessageBox(object):
    """
    Geeft een bericht weer op het scherm.
    """
    def __init__(self, raw_text, face_image=None, spr_image=None, scr_capt=None, sound=SFX.message,
                 last=False, callback=None, no_key=False, name=GameState.MessageBox):
        """
        :param raw_text: dit is een list die aangeleverd moet worden. Als het alleen een string is, dan wordt het
        een plaatje die gebruikt maakt van face_image.
        :param spr_image: list van loaded images
        :param scr_capt: een vorige scr_capt meegeven, niets meegeven = nieuwe capt, False = zwart scherm.
        :param last: is het de laatste msgbox uit een reeks? True of False. Geef dan het afsluit geluidje 'done'.
        """
        self.sound = sound
        self.audio_first_time = False
        self.last = last
        self.screen = pygame.display.get_surface()
        self.name = name

        if scr_capt is None:
            self.scr_capt = ScreenCapture()
        elif scr_capt is False:
            self.scr_capt = ScreenCapture(black_background=True)
        else:
            self.scr_capt = scr_capt

        if self.name == GameState.LoadScreen:
            self.animation = Animation()
            self.anim_space = ICONW
        else:
            self.animation = None
            self.anim_space = 0

        self.callback = callback
        self.no_key = no_key

        self.font = pygame.font.SysFont(FONT, FONTSIZE)

        # een plaatje alleen is een string en geen list. zet dus om indien nodig.
        if type(raw_text) == list:
            self.raw_text = raw_text
        else:
            self.raw_text = [""]
            face_image = raw_text
            raw_text = [""]

        self.vis_text = []
        self.face_image = face_image
        self.face_image_width = 0
        self.face_image_height = 0
        self.spr_image = spr_image
        self.spr_img_space = 0
        if self.face_image:
            self.face_image = pygame.image.load(face_image).convert_alpha()
            self.face_image_width = self.face_image.get_width()
            self.face_image_height = self.face_image.get_height()
        if self.spr_image:
            self.spr_img_space = self.spr_image[0].get_width()  # de breedte van de eerste uit de list

        text_widths = []
        for row in raw_text:
            self.vis_text.append(self.font.render(row, True, FONTCOLOR).convert_alpha())
            text_widths.append(self.font.render(row, True, FONTCOLOR).get_width())
        box_width = max(text_widths) + FONTPOSX * 2 + self.face_image_width + self.spr_img_space + self.anim_space
        box_height = len(self.vis_text) * LINEHEIGHT + FONTPOSY * 2
        if box_height < self.face_image_height + FACEPOSY * 2:
            box_height = self.face_image_height + FACEPOSY * 2

        self.surface = pygame.Surface((box_width, box_height))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)

        self.surface.fill(BACKGROUNDCOLOR)
        self.surface.set_colorkey(BACKGROUNDCOLOR)

        self.background = pygame.image.load(MESSAGESPRITE).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.surface.get_size())

    def _has_no_text(self):
        return self.raw_text == [""]

    def single_input(self, event, gamestate, audio):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        :param gamestate:
        :param audio:
        """
        if self.no_key:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == Keys.Exit.value:
                self._exit(gamestate, audio)
            elif event.key in Keys.Select.value:
                self._exit(gamestate, audio)
            # elif event.key == Keys.Action.value:  # todo, voorlopig uitgezet dat je met de action knop verder kan
            #     self._exit(gamestate, audio)      # klikken. dit is vanwege langzamere computers.
        elif event.type == pygame.MOUSEBUTTONDOWN:  # anders druk je te vaak op a. definitieve oplossing verzinnen.
            if event.button == Keys.Leftclick.value:
                self._exit(gamestate, audio)

    def _exit(self, gamestate, audio):
        if self.last:
            audio.play_sound(SFX.done)
        gamestate.pop()

    def render(self):
        """
        Teken de tekst.
        """
        self.scr_capt.render()

        self.surface.blit(self.background, (0, 0))

        if self.face_image:
            if self._has_no_text():
                self.surface.blit(self.face_image, (FULLPOSX, FACEPOSY))
            else:
                self.surface.blit(self.face_image, (FACEPOSX, FACEPOSY))

        if self.spr_image:
            for i, line in enumerate(self.spr_image):
                self.surface.blit(line, (IMGPOSX, IMGPOSY + i * LINEHEIGHT))

        for i, line in enumerate(self.vis_text):
            if i == 0:
                self.surface.blit(line, (FONTPOSX + self.face_image_width,
                                         FONTPOSY + i * LINEHEIGHT))
            else:
                self.surface.blit(line, (FONTPOSX + self.face_image_width + self.spr_img_space,
                                         FONTPOSY + i * LINEHEIGHT))

        if self.animation:
            self.animation.render(self.surface)

        self.screen.blit(self.surface, self.rect.topleft)

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def multi_input(self, key_input, mouse_pos, dt):
        if self.no_key:
            return

    def update(self, dt, gamestate, audio):
        """
        Laat een evt geluid horen, eenmalig.
        """
        if self.sound:
            if self.audio_first_time is False:
                self.audio_first_time = True
                audio.play_sound(self.sound)

        if self.animation:
            self.animation.update(dt)


class LoadScreen(MessageBox):
    """..."""
    def __init__(self):
        # noinspection PyTypeChecker
        super().__init__(["Loading world..."], scr_capt=False, sound=None, no_key=True, name=GameState.LoadScreen)


class Animation(object):
    """..."""
    def __init__(self):
        self.east_states = {0: (32, 64, 32, 32), 1: (0, 64, 32, 32), 2: (32, 64, 32, 32), 3: (64, 64, 32, 32)}
        self.timer = 0
        self.step = 0

        self.full_sprite = pygame.image.load(PATH).convert_alpha()
        self.full_sprite.set_clip(self.east_states[self.step])
        self.image = self.full_sprite.subsurface(self.full_sprite.get_clip())

    def update(self, dt):
        """..."""
        self.timer += dt
        if self.timer > TIME:
            self.timer = 0
            self.step += 1
            if self.step >= len(self.east_states):
                self.step = 0

        self.full_sprite.set_clip(self.east_states[self.step])
        self.image = self.full_sprite.subsurface(self.full_sprite.get_clip())

    def render(self, screen):
        """..."""
        screen.blit(self.image, (ICONX, ICONY))
