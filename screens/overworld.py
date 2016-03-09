
"""
class: Overworld
"""

import pygame

import keys
import screens.menu.manager
import screens.party.display
import screens.sprites
import screens.window
import statemachine


WINDOWWIDTH = 800
WINDOWHEIGHT = 600
WINDOWPOS = 100, 100

BACKGROUNDCOLOR = pygame.Color("black")

INVLBL = "I"
UPLBL = "Up"
DOWNLBL = "Down"
LEFTLBL = "Left"
RIGHTLBL = "Right"

BTNWIDTH = 40
BTNHEIGHT = 40

INVX, INVY = -200, -300
UPX, UPY = -150, -300
DOWNX, DOWNY = -150, -250
LEFTX, LEFTY = -200, -250
RIGHTX, RIGHTY = -100, -250


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
        self.window = screens.window.Window(WINDOWWIDTH, WINDOWHEIGHT, self.engine)

        self.name = statemachine.States.Overworld

        self.buttons = None
        self._init_buttons()
        self.key_input = None       # dit is voor de mousepress op een button.

    def _init_buttons(self):
        """
        Maak de knoppen aan en zet ze in een lijst.
        Plaats ook de bijbehorende keys in een lijst.
        """
        bg_width = self.background.get_width()
        bg_height = self.background.get_height()

        # todo, afhankelijk van situatie, buttons niet weergeven
        # button_view = sprites.ButtonSprite((bg_width-200,   bg_height-300), "V",     pygame.K_v)
        button_inv = screens.sprites.ButtonSprite(
                                    BTNWIDTH, BTNHEIGHT, (bg_width + INVX,   bg_height + INVY),   INVLBL,   keys.INV)
        button_up = screens.sprites.ButtonSprite(
                                    BTNWIDTH, BTNHEIGHT, (bg_width + UPX,    bg_height + UPY),    UPLBL,    keys.UP)
        button_down = screens.sprites.ButtonSprite(
                                    BTNWIDTH, BTNHEIGHT, (bg_width + DOWNX,  bg_height + DOWNY),  DOWNLBL,  keys.DOWN)
        button_left = screens.sprites.ButtonSprite(
                                    BTNWIDTH, BTNHEIGHT, (bg_width + LEFTX,  bg_height + LEFTY),  LEFTLBL,  keys.LEFT)
        button_right = screens.sprites.ButtonSprite(
                                    BTNWIDTH, BTNHEIGHT, (bg_width + RIGHTX, bg_height + RIGHTY), RIGHTLBL, keys.RIGHT)
        # button_cancel = sprites.ButtonSprite((bg_width-100, bg_height-200), "C",     pygame.K_c)

        # self.buttons = [button_view, button_up, button_down, button_left, button_right, button_cancel]
        self.buttons = [button_inv, button_up, button_down, button_left, button_right]

    def on_enter(self):
        """
        Wanneer deze state op de stack komt, voer dit uit.
        Zet muziek en achtergrond geluiden indien nodig.
        """
        self.engine.audio.set_bg_music(self.name)
        self.engine.audio.set_bg_sounds(self.name)

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == keys.LEFTCLICK:
                for button in self.buttons:
                    button_press = button.single_click(event)
                    if button_press == keys.INV:
                        self._show_party_screen()
                        break

        elif event.type == pygame.KEYDOWN:
            if event.key == keys.INV:
                self._show_party_screen()
            elif event.key == keys.EXIT:
                self._show_pause_menu()
            self.window.single_input(event)

    def multi_input(self, key_input, mouse_pos, dt):
        """
        Registreert of er op de buttons wordt geklikt. En zet dat om naar keyboard input.
        :param key_input: pygame.key.get_pressed()
        :param mouse_pos: pygame.mouse.get_pos()
        :param dt: self.clock.tick(FPS)/1000.0
        """
        self.key_input = key_input

        for button in self.buttons:
            self.key_input = button.multi_click(mouse_pos, self.key_input)

        self.window.multi_input(self.key_input, mouse_pos, dt)

    def update(self, dt):
        """
        Update de window.
        :param dt: self.clock.tick(FPS)/1000.0
        """
        self.window.update(dt)

        for button in self.buttons:
            button.update(self.key_input)

    def render(self):
        """
        Handel de view af in de window -> teken de achtergrond -> teken de window -> teken de buttons.
        """
        self.window.render()

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.window.surface, WINDOWPOS)

        for button in self.buttons:
            button.render(self.screen)

    def _show_pause_menu(self):
        self.engine.audio.play_sound(self.engine.audio.select)

        push_object = screens.menu.manager.create_menu(statemachine.States.PauseMenu, self.engine)
        self.engine.gamestate.push(push_object)

    def _show_party_screen(self):
        push_object = screens.party.display.Display(self.screen, self.engine)
        self.engine.gamestate.push(push_object)
