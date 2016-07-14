
"""
class: InputBox
"""

import pygame

from constants import Keys

BOXWIDTH = 360
BOXHEIGHT = 53
BOXY = 200

BACKGROUNDCOLOR = pygame.Color("black")
RECTCOLOR = pygame.Color("white")

INPUTLABEL = "Name: "
INPUTLENGTH = 8

FONT = None
FONTSIZE = 50
FONTCOLOR = pygame.Color("white")
FONTPOS = 10, 10


class InputBox(object):
    """
    Geeft een input box weer om te kunnen typen.
    """
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.surface = pygame.Surface((BOXWIDTH, BOXHEIGHT))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.screen.get_width() - BOXWIDTH) / 2, BOXY

        self.font = pygame.font.SysFont(FONT, FONTSIZE)
        self.namelabel = INPUTLABEL
        self.textbox = ["_"]

        self.running = False
        self.confirm = False

    def input_loop(self):
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

        if self.confirm:
            return "".join(self.textbox[0:-1])  # return de string maar zonder het laatste character
        else:
            return None

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        valid_characters = "1234567890abcdefghijklmnopqrstuvwxyz"
        if event.type == pygame.KEYDOWN:
            if len(self.textbox) <= INPUTLENGTH:
                if event.unicode in valid_characters:
                    self.textbox.insert(-1, event.unicode)
            if event.key == Keys.Remove.value:
                if len(self.textbox) > 1:
                    del self.textbox[-2]
                elif len(self.textbox) == 0:
                    self.textbox = ["_"]
            elif event.key == Keys.Exit.value:
                self.running = False
            elif event.key in Keys.Select.value:
                self.confirm = True
                self.running = False

    def render(self):
        """
        Teken de letters.
        """
        self.surface.fill(BACKGROUNDCOLOR)
        pygame.draw.rect(self.surface, RECTCOLOR, self.surface.get_rect(), 1)
        self.surface.blit(
            self.font.render(self.namelabel + "".join(self.textbox), True, FONTCOLOR).convert_alpha(), FONTPOS)
        self.screen.blit(self.surface, self.rect.topleft)
