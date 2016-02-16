
"""
class: Overworld
"""

import pygame

import screens.party.display
import screens.sprites
import screens.window
import states


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
        self.window = screens.window.Window(WINDOWWIDTH, WINDOWHEIGHT, self.engine.audio)

        self.partyscreen = None

        self.buttons = None
        self._init_buttons()
        self.key_input = pygame.key.get_pressed()       # dit is voor de mousepress op een button.

    def _init_buttons(self):
        """
        Maak de knoppen aan en zet ze in een lijst.
        Plaats ook de bijbehorende keys in een lijst.
        """
        bg_width = self.background.get_width()
        bg_height = self.background.get_height()

        # todo, afhankelijk van situatie, buttons niet weergeven
        # button_view = sprites.ButtonSprite((bg_width-200,   bg_height-300), "V",     pygame.K_v)
        button_i = screens.sprites.ButtonSprite(40, 40, (bg_width - 200, bg_height - 300), "I", pygame.K_i)
        button_up = screens.sprites.ButtonSprite(40, 40, (bg_width - 150, bg_height - 300), "Up", pygame.K_UP)
        button_down = screens.sprites.ButtonSprite(40, 40, (bg_width - 150, bg_height - 250), "Down", pygame.K_DOWN)
        button_left = screens.sprites.ButtonSprite(40, 40, (bg_width - 200, bg_height - 250), "Left", pygame.K_LEFT)
        button_right = screens.sprites.ButtonSprite(40, 40, (bg_width - 100, bg_height - 250), "Right", pygame.K_RIGHT)
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
        if self.engine.currentstate == states.GameState.Overworld:
            self.key_input = key_input

            for button in self.buttons:
                self.key_input = button.multi_click(mouse_pos, self.key_input)

            self.window.handle_multi_input(self.key_input, dt)

        elif self.engine.currentstate == states.GameState.PartyScreen:
            self.partyscreen.handle_multi_input(key_input, mouse_pos)

    def handle_single_mouse_input(self, event):
        """
        Handelt mouse events af.
        :param event: pygame.MOUSEBUTTONDOWN uit engine.py
        """
        if self.engine.currentstate == states.GameState.Overworld:

            if event.button == 1:
                for button in self.buttons:
                    button_press = button.single_click(event)
                    if button_press == pygame.K_i:
                        self._show_party_screen()
                        break

        elif self.engine.currentstate == states.GameState.PartyScreen:

            if self.partyscreen.handle_single_mouse_input(event):       # alleen de ESC key returned een waarde
                self._close_party_screen()

    def handle_single_keyboard_input(self, event):
        """
        Handelt keyboard events af.
        :param event: pygame.KEYDOWN uit engine.py
        """
        if self.engine.currentstate == states.GameState.Overworld:

            if event.key == pygame.K_i:
                self._show_party_screen()

            self.window.handle_single_input(event)

        elif self.engine.currentstate == states.GameState.PartyScreen:

            self.partyscreen.handle_single_keyboard_input(event)

            if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                self._close_party_screen()

    def _show_party_screen(self):
        self.engine.statemachine.push(states.GameState.PartyScreen)
        self.partyscreen = screens.party.display.Display(self.engine.data, self.screen)

    def _close_party_screen(self):
        self.engine.statemachine.pop(self.engine.currentstate)
        self.partyscreen = None
