
"""
class: InputBox
"""

import pygame

import keys

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
    def __init__(self, engine, name):
        self.engine = engine
        self.screen = self.engine.screen
        self.surface = pygame.Surface((BOXWIDTH, BOXHEIGHT))
        self.surface = self.surface.convert()
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.screen.get_width() - BOXWIDTH) / 2, BOXY

        self.name = name

        self.font = pygame.font.SysFont(FONT, FONTSIZE)
        self.namelabel = INPUTLABEL
        self.textbox = ["_"]

    # noinspection PyMethodMayBeStatic
    def on_enter(self):
        """
        Wanneer deze state op de stack komt, voer dit uit.
        Op dit moment nog niets echts
        """
        pass

    # noinspection PyMethodMayBeStatic
    def on_exit(self):
        """
        Wanneer deze state onder een andere state van de stack komt, voer dit uit.
        Op dit moment nog niets echts
        """
        pass

    def single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.KEYDOWN:
            if len(self.textbox) <= INPUTLENGTH:
                if 48 <= event.key <= 57 or 97 <= event.key <= 122:
                    self.textbox.insert(-1, event.unicode)
            if event.key == keys.REMOVE:
                if len(self.textbox) > 1:
                    self.textbox.pop(-2)
                if len(self.textbox) == 0:
                    self.textbox = ["_"]
            if event.key == keys.EXIT:
                self.engine.gamestate.pop()
            if event.key in keys.SELECT:
                self.engine.gamestate.pop()
                return "piet"   # todo, hoe geef ik het juiste goed terug?
                # piet = self.engine.gamestate.deep_peek()
                # pass

    # noinspection PyMethodMayBeStatic
    def multi_input(self, key_input, mouse_pos, dt):
        """
        Handelt de ingedrukt-houden muis en keyboard input af.
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    # noinspection PyMethodMayBeStatic
    def update(self, dt):
        """
        Update de waarden van de bovenste state.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        pass

    def render(self):
        """
        Teken de data.
        """
        self.surface.fill(BACKGROUNDCOLOR)
        pygame.draw.rect(self.surface, RECTCOLOR, self.surface.get_rect(), 1)
        self.surface.blit(
            self.font.render(self.namelabel + "".join(self.textbox), True, FONTCOLOR).convert_alpha(), FONTPOS)
        self.screen.blit(self.surface, self.rect.topleft)
