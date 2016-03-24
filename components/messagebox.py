
"""
class: MessageBox
"""

import pygame

import components.screencapture
import keys

BACKGROUNDCOLOR = pygame.Color("black")

FONT = None
FONTSIZE = 30
FONTCOLOR = pygame.Color("black")
FONTPOSX = 40
FONTPOSY = 40
LINEHEIGHT = 25

MESSAGESPRITE = 'resources/sprites/messagebox.png'


class MessageBox(object):
    """
    Geeft een bericht weer op het scherm.
    """
    def __init__(self, message):
        self.screen = pygame.display.get_surface()

        self.scr_capt = components.screencapture.ScreenCapture()

        self.font = pygame.font.SysFont(FONT, FONTSIZE)
        self.textbox = message

        self.running = False

        text_widths = []
        for row in self.textbox:
            text_widths.append(self.font.render(row, True, FONTCOLOR).get_width())
        box_width = max(text_widths) + FONTPOSX * 2
        box_height = len(self.textbox) * LINEHEIGHT + FONTPOSY * 2

        self.surface = pygame.Surface((box_width, box_height))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)

        self.surface.fill(BACKGROUNDCOLOR)
        self.surface.set_colorkey(BACKGROUNDCOLOR)

        self.image = pygame.image.load(MESSAGESPRITE).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.surface.get_size())

    def message_loop(self):
        """
        De loop waarin hij blijft, totdat de juiste input komt.
        """
        self.running = True
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.single_input(event)

            self.render()
            pygame.display.update()

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.KEYDOWN:
            if event.key == keys.EXIT:
                self.running = False
            if event.key in keys.SELECT:
                self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == keys.LEFTCLICK:
                self.running = False

    def render(self):
        """
        Teken de tekst.
        """
        self.scr_capt.render()

        self.surface.blit(self.image, (0, 0))

        for i, line in enumerate(self.textbox):
            label = self.font.render(line, True, FONTCOLOR).convert_alpha()
            self.surface.blit(label, (FONTPOSX, FONTPOSY + i * LINEHEIGHT))

        self.screen.blit(self.surface, self.rect.topleft)
