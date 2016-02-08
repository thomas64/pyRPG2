
"""
class: GameEngine
"""

import pygame

import console
import data
import loadsave
import menu
import menus
import overworld
import audio
import statemachine
import states

FPS = 60        # minimaal 15, anders kan hij door bomen lopen

DEBUGKEY = pygame.K_F12
DEBUGFONT = 'courier'
DEBUGFONTSIZE = 11
DEBUGFONTCOLOR = pygame.Color("white")


class GameEngine(object):
    """
    De grafische weergave van het scherm.
    """
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.state = statemachine.StateMachine()
        self.data = data.Data()
        self.audio = audio.Audio()

        self.running = False

        self.clock = pygame.time.Clock()
        self.playtime = 0.0
        self.dt = 0.0
        self.timer = 0.0

        self.mainmenu = None
        self.pausemenu = None
        self.optionsmenu = None
        self.loadsave = None
        self.overworld = None

        self.debugfont = pygame.font.SysFont(DEBUGFONT, DEBUGFONTSIZE)
        self.currentstate = None
        self.key_input = None
        self.scr_capt = None

        self.show_debug = False

    def main_loop(self):
        """
        Start de game loop.
        """
        self.running = True
        self._show_main_menu()

        while self.running:
            self.dt = self.clock.tick(FPS)/1000.0       # limit the redraw speed to 60 frames per second
            self.playtime += self.dt

            self.currentstate = self.state.peek()
            self.handle_view()
            self.handle_multi_input()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_single_input(event)
            pygame.display.flip()

    def handle_view(self):
        """
        Laat de weergave van de verschillende states zien.
        """
        def _show_debug():
            if self.show_debug:
                text = (
                    "FPS:              {:.2f}".format(self.clock.get_fps()),
                    "dt:               {:.3f}".format(self.dt),
                    "playtime:         {:.2f}".format(self.playtime)
                )
                try:
                    hero = self.overworld.window.hero
                    text2 = (
                        "zoom:             {:.1f}".format(self.overworld.window.map1.map_layer.zoom),
                        "time_up:          {}".format(hero.time_up),
                        "time_down:        {}".format(hero.time_down),
                        "time_left:        {}".format(hero.time_left),
                        "time_right:       {}".format(hero.time_right),
                        "time_delay:       {}".format(hero.time_delay),
                        "last_direction:   {}".format(hero.last_direction),
                        "move_direction:   {}".format(hero.move_direction),
                        "movespeed:        {}".format(hero.movespeed),
                        "old_position.x:   {}".format(hero.old_position[0]),
                        "old_position.y:   {}".format(hero.old_position[1]),
                        "new_position.x:   {}".format(hero.rect.x),
                        "new_position.y:   {}".format(hero.rect.y),
                        "true_position.x:  {}".format(hero.true_position[0]),
                        "true_position.y:  {}".format(hero.true_position[1]),
                        "step_count:       {}".format(hero.step_count),
                        "step_animation:   {}".format(hero.step_animation)
                    )
                    text += text2
                except AttributeError:
                    pass
                for count, line in enumerate(text):
                    self.screen.blit(self.debugfont.render(line, True, DEBUGFONTCOLOR), (0, count * 10))

        if self.currentstate == states.GameState.MainMenu:
            self.mainmenu.handle_view()                         # geen achtergrond
        elif self.currentstate == states.GameState.OptionsMenu:
            self.optionsmenu.handle_view()
        elif self.currentstate == states.GameState.PauseMenu:
            self.pausemenu.handle_view(self.scr_capt)           # achtergrond, screen capture
        elif self.currentstate == states.GameState.Overworld or \
                self.currentstate == states.GameState.PartyScreen:
            self.overworld.handle_view()

        _show_debug()

    def handle_multi_input(self):
        """
        Handelt de ingedrukt-houden muis en keyboard input af.
        """
        self.key_input = pygame.key.get_pressed()

        if self.currentstate == states.GameState.Overworld:
            mouse_pos = None
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
            self.overworld.handle_multi_input(self.key_input, mouse_pos, self.dt)

    def handle_single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            console.mouse_down(event.pos, event.button)
        if event.type == pygame.KEYDOWN:
            console.keyboard_down(event.key, event.unicode)

            if event.key == DEBUGKEY:
                self.show_debug ^= True                     # simple boolean swith

            if self.currentstate == states.GameState.MainMenu:          # eerst de keys op het toetsenbord
                if event.key == pygame.K_ESCAPE:
                    self._main_menu_select_exit_game(with_esc=True)
                    return                                              # returns, want anders zitten ze
            elif self.currentstate == states.GameState.OptionsMenu:     # de menu's in de weg
                if event.key == pygame.K_ESCAPE:
                    self._options_menu_select_back(with_esc=True)
                    return
            elif self.currentstate == states.GameState.PauseMenu:
                if event.key == pygame.K_ESCAPE:
                    self._pause_menu_select_continue(with_esc=True)
                    return
            elif self.currentstate == states.GameState.Overworld:
                self.overworld.handle_single_input(event)
                if event.key == pygame.K_ESCAPE:
                    self._show_pause_menu()
                if event.key == pygame.K_BACKSPACE:
                    self._kill_game()                           # todo, deze en de methode moeten uiteindelijk weg

        if self.currentstate == states.GameState.MainMenu:              # dan de menu's
            menu_choice = self.mainmenu.handle_single_input(event)
            if menu_choice == menus.Main().NewGame:
                self._main_menu_select_new_game()
            elif menu_choice == menus.Main().LoadGame:
                self._main_menu_select_load_game()
            elif menu_choice == menus.Main().Options:
                self._main_menu_select_options()
            elif menu_choice == menus.Main().ExitGame:
                self._main_menu_select_exit_game()

        elif self.currentstate == states.GameState.OptionsMenu:
            menu_choice = self.optionsmenu.handle_single_input(event)
            if menu_choice == menus.Options().Music:
                self._options_menu_select_music()
            elif menu_choice == menus.Options().Sound:
                self._options_menu_select_sound()
            elif menu_choice == menus.Options().Back:
                self._options_menu_select_back()

        elif self.currentstate == states.GameState.PauseMenu:
            menu_choice = self.pausemenu.handle_single_input(event)
            if menu_choice == menus.Pause().ContinueGame:
                self._pause_menu_select_continue()
            elif menu_choice == menus.Pause().SaveGame:
                self._pause_menu_select_save_game()
            elif menu_choice == menus.Pause().MainMenu:
                self._pause_menu_select_main_menu()

    def _show_main_menu(self):
        self.pausemenu = None
        self.scr_capt = None
        self.overworld = None
        self.state.clear()
        self.state.push(states.GameState.MainMenu)
        self.mainmenu = menu.GameMenu(self.screen, self.audio, menus.Main(), True)
        self.audio.play_music(self.audio.mainmenu)

    def _main_menu_select_new_game(self):
        self.mainmenu = None
        self.state.pop(self.currentstate)
        self.state.push(states.GameState.Overworld)
        self.overworld = overworld.Overworld(self)
        self.audio.play_music(self.audio.overworld)

    def _main_menu_select_load_game(self):
        self.loadsave = loadsave.Dialog(self)
        self.overworld = overworld.Overworld(self)                                  # laad de overworld alvast
        if self.loadsave.load() is None:
            self.overworld = None                                                   # toch niet
        else:                                                                       # geef dan data mee aan de overworld
            self.audio.play_sound(self.audio.select)
            self.mainmenu = None
            self.state.pop(self.currentstate)
            self.state.push(states.GameState.Overworld)
            self.audio.play_music(self.audio.overworld)
        pygame.event.clear()
        self.loadsave = None

    def _main_menu_select_options(self):
        self._show_options_menu()

    def _main_menu_select_exit_game(self, with_esc=False):
        if with_esc:
            self.audio.play_sound(self.audio.select)
        self.audio.fade_music()
        self.running = False

    def _show_options_menu(self):
        self.state.push(states.GameState.OptionsMenu)
        menu_items = menus.Options(self.audio.music, self.audio.sound)              # hier worden de options geschreven
        self.optionsmenu = menu.GameMenu(self.screen, self.audio, menu_items, True)

    def _options_menu_select_music(self):
        settingview = self.optionsmenu.menu_texts[self.optionsmenu.cur_item]        # hier wordt de visualisatie
        if self.audio.music == 1:
            settingview.text = settingview.text.replace("On", "Off")                # later aangepast
            self.audio.music = 0
            self.audio.current.stop()
        else:
            settingview.text = settingview.text.replace("Off", "On")
            self.audio.music = 1
            self.audio.play_music(self.audio.mainmenu)
        self.audio.write_cfg()

    def _options_menu_select_sound(self):
        settingview = self.optionsmenu.menu_texts[self.optionsmenu.cur_item]
        if self.audio.sound == 1:
            settingview.text = settingview.text.replace("On", "Off")
            self.audio.sound = 0
        else:
            settingview.text = settingview.text.replace("Off", "On")
            self.audio.sound = 1
        self.audio.write_cfg()

    def _options_menu_select_back(self, with_esc=False):
        if with_esc:
            self.audio.play_sound(self.audio.select)
        self.state.pop(self.currentstate)
        self.optionsmenu = None

    def _show_pause_menu(self):
        self.audio.play_sound(self.audio.select)
        self.audio.fade_music()
        scr_data = pygame.image.tostring(self.screen, 'RGBA')       # maak een screen capture
        self.scr_capt = pygame.image.frombuffer(scr_data, self.screen.get_size(), 'RGBA')
        self.state.push(states.GameState.PauseMenu)
        self.pausemenu = menu.GameMenu(self.screen, self.audio, menus.Pause(), False)

    def _pause_menu_select_continue(self, with_esc=False):
        if with_esc:
            self.audio.play_sound(self.audio.select)            # omdat escape in menu standaard geen geluid geeft
        self.state.pop(self.currentstate)
        self.pausemenu = None
        self.scr_capt = None
        self.audio.play_music(self.audio.overworld)

    def _pause_menu_select_save_game(self):
        self.loadsave = loadsave.Dialog(self)
        if self.loadsave.save():
            self.audio.play_sound(self.audio.select)
        pygame.event.clear()                                    # anders stapelen de geluiden zich op
        self.loadsave = None

    def _pause_menu_select_main_menu(self):
        self._show_main_menu()

    @staticmethod
    def _kill_game():
        import sys
        pygame.quit()
        sys.exit()
