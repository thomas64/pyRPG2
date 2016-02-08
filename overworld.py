
"""
class: Overworld
"""

import pygame

import partyscreen
import sprites
import states
import window


WINDOWWIDTH = 800
WINDOWHEIGHT = 600
WINDOWPOS = 100, 100

BACKGROUNDCOLOR = pygame.Color("black")


class Overworld(object):
    """
    Overworld layout.
    """
    def __init__(self, engine):
        self.engine = engine
        self.screen = self.engine.screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()
        self.window = window.Window(WINDOWWIDTH, WINDOWHEIGHT, self.engine.audio)

        self.partyscreen = None

        self.buttons = None
        self._init_buttons()
        self.key_input = pygame.key.get_pressed()

    def _init_buttons(self):
        """
        Maak de knoppen aan en zet ze in een lijst.
        Plaats ook de bijbehorende keys in een lijst.
        """
        bg_width = self.background.get_width()
        bg_height = self.background.get_height()

        # todo, afhankelijk van situatie, buttons niet weergeven
        # button_view = sprites.ButtonSprite((bg_width-200,   bg_height-300), "V",     pygame.K_v)
        button_i = sprites.ButtonSprite((bg_width-200,      bg_height-300), "I",     pygame.K_i)
        button_up = sprites.ButtonSprite((bg_width-150,     bg_height-300), "Up",    pygame.K_UP)
        button_down = sprites.ButtonSprite((bg_width-150,   bg_height-250), "Down",  pygame.K_DOWN)
        button_left = sprites.ButtonSprite((bg_width-200,   bg_height-250), "Left",  pygame.K_LEFT)
        button_right = sprites.ButtonSprite((bg_width-100,  bg_height-250), "Right", pygame.K_RIGHT)
        # button_cancel = sprites.ButtonSprite((bg_width-100, bg_height-200), "C",     pygame.K_c)

        # self.buttons = [button_view, button_up, button_down, button_left, button_right, button_cancel]
        self.buttons = [button_i, button_up, button_down, button_left, button_right]

    def handle_view(self):
        """
        Handel de view af in de window -> teken de achtergrond -> teken de window -> teken de buttons.
        """
        if self.engine.currentstate == states.GameState.Overworld:

            self.window.handle_view()

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.window.surface, WINDOWPOS)

            for button in self.buttons:
                button.draw(self.screen, self.key_input)

        elif self.engine.currentstate == states.GameState.PartyScreen:
            self.partyscreen.handle_view()

    def handle_multi_input(self, key_input, mouse_pos, dt):
        """
        Registreert of er op de buttons wordt geklikt. En zet dat om naar keyboard input.
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        self.key_input = key_input

        for button in self.buttons:
            self.key_input = button.click(mouse_pos, self.key_input)

        self.window.handle_multi_input(self.key_input, dt)

    def handle_single_input(self, event):
        """
        Handelt keyevents af.
        :param event: pygame.event.get() uit overworld.py
        """
        if event.key == pygame.K_i:
            self.engine.state.push(states.GameState.PartyScreen)
            self.engine.audio.fade_music()
            self.partyscreen = partyscreen.PartyScreen(self.screen)

        self.window.handle_single_input(event)
