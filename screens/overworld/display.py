
"""
class: Display
"""

import pygame

import audio as sfx
from components import Button
import keys
import screens.menu.manager
import screens.party.display
import screens.overworld.window
from statemachine import GameState


WINDOWPOS = 10, 40

BACKGROUNDCOLOR = pygame.Color("black")
LINECOLOR = pygame.Color("white")

MAPTITLEFONT = None
MAPTITLEFONTSIZE = 30
MAPTITLEFONTCOLOR = pygame.Color("white")
MAPTITLEPOS = 100, 10

ACTLBL = "A"
INVLBL = "I"
UPLBL = "Up"
DOWNLBL = "Down"
LEFTLBL = "Left"
RIGHTLBL = "Right"

BTN_W = 40
BTN_H = 40

ACTX, ACTY = -200, -300
INVX, INVY = -100, -300
UPX, UPY = -150, -300
DOWNX, DOWNY = -150, -250
LEFTX, LEFTY = -200, -250
RIGHTX, RIGHTY = -100, -250


class Display(object):
    """
    Overworld layout.
    """
    def __init__(self, engine):
        self.engine = engine
        self.screen = pygame.display.get_surface()
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BACKGROUNDCOLOR)
        self.background = self.background.convert()
        self.window = screens.overworld.window.Window(self.engine)

        self.map_title_font = pygame.font.SysFont(MAPTITLEFONT, MAPTITLEFONTSIZE)
        self.map_title_label = ""
        self.name = GameState.Overworld

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
        # button_view = sprites.Button((bg_width-200,   bg_height-300), "V",     pygame.K_v)
        button_act = Button(BTN_W,   BTN_H, (bg_width + ACTX,   bg_height + ACTY),   ACTLBL,   keys.ACTION)
        button_inv = Button(BTN_W,   BTN_H, (bg_width + INVX,   bg_height + INVY),   INVLBL,   keys.INV)
        button_up = Button(BTN_W,    BTN_H, (bg_width + UPX,    bg_height + UPY),    UPLBL,    keys.UP)
        button_down = Button(BTN_W,  BTN_H, (bg_width + DOWNX,  bg_height + DOWNY),  DOWNLBL,  keys.DOWN)
        button_left = Button(BTN_W,  BTN_H, (bg_width + LEFTX,  bg_height + LEFTY),  LEFTLBL,  keys.LEFT)
        button_right = Button(BTN_W, BTN_H, (bg_width + RIGHTX, bg_height + RIGHTY), RIGHTLBL, keys.RIGHT)
        # button_cancel = sprites.Button((bg_width-100, bg_height-200), "C",     pygame.K_c)

        # self.buttons = [button_view, button_up, button_down, button_left, button_right, button_cancel]
        self.buttons = [button_act, button_inv, button_up, button_down, button_left, button_right]

    def on_enter(self):
        """
        Wanneer deze state op de stack komt, voer dit uit.
        Zet muziek en achtergrond geluiden indien nodig.
        """
        self.engine.audio.set_bg_music(self.name)
        self.engine.audio.set_bg_sounds(self.name)

        self.window.on_enter()

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

        self.map_title_label = self.map_title_font.render(self.engine.current_map.title,
                                                          True, MAPTITLEFONTCOLOR).convert_alpha()
        for button in self.buttons:
            button.update(self.key_input)

    def render(self):
        """
        Handel de view af in de window -> teken de achtergrond -> teken de window -> teken de buttons.
        """
        self.window.render()
        # lijn om de window
        # pygame.draw.rect(
        #     self.background, LINECOLOR, (WINDOWPOS[0]-1, WINDOWPOS[1]-1, WINDOWWIDTH+2, WINDOWHEIGHT+2), 1)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.window.surface, WINDOWPOS)

        self.screen.blit(self.map_title_label, MAPTITLEPOS)

        for button in self.buttons:
            button.render(self.screen)

    def _show_pause_menu(self):
        self.engine.audio.play_sound(sfx.MENUSELECT)

        push_object = screens.menu.manager.create_menu(GameState.PauseMenu, self.engine)
        self.engine.gamestate.push(push_object)

    def _show_party_screen(self):
        push_object = screens.party.display.Display(self.engine)
        self.engine.gamestate.push(push_object)
