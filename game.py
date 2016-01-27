
"""
class: GameEngine
"""

import pygame

import loadsave
import menu
import menus
import overworld
import sound
import statemachine
import states

FPS = 60        # minimaal 20 en maximaal 130, anders komen er bugs voor.

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
        self.sound = sound.Sound()

        self.running = False

        self.clock = pygame.time.Clock()
        self.playtime = 0.0
        self.dt = 0.0
        self.timer = 0.0

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
        def show_debug():
            """
            Geeft debug informatie weer linksboven in het scherm.
            """
            if self.show_debug:
                # hero = self.overworld.hero
                text = ("FPS:              {:.2f}".format(self.clock.get_fps()),
                        "dt:               {:.3f}".format(self.dt),
                        "playtime:         {:.2f}".format(self.playtime),
                        # "time_up:          {}".format(hero.time_up),
                        # "time_down:        {}".format(hero.time_down),
                        # "time_left:        {}".format(hero.time_left),
                        # "time_right:       {}".format(hero.time_right),
                        # "time_delay:       {}".format(hero.time_delay),
                        # "last_direction:   {}".format(hero.last_direction),
                        # "move_direction:   {}".format(hero.move_direction),
                        # "movespeed:        {}".format(hero.movespeed),
                        # "old_position.x:   {}".format(hero.old_position[0]),
                        # "old_position.y:   {}".format(hero.old_position[1]),
                        # "new_position.x:   {}".format(hero.rect.x),
                        # "new_position.y:   {}".format(hero.rect.y),
                        # "true_position.x:  {}".format(hero.true_position[0]),
                        # "true_position.y:  {}".format(hero.true_position[1]),
                        # "step_count:       {}".format(hero.step_count),
                        # "step_animation:   {}".format(hero.step_animation),
                        )
                for count, line in enumerate(text):
                    self.screen.blit(self.debugfont.render(line, True, DEBUGFONTCOLOR), (0, count * 10))

        if self.currentstate == states.GameState.MainMenu:
            self.mainmenu.handle_view(None)                 # geen achtergrond
            show_debug()
        elif self.currentstate == states.GameState.OptionsMenu:
            self.optionsmenu.handle_view(None)
        elif self.currentstate == states.GameState.PauseMenu:
            self.pausemenu.handle_view(self.scr_capt)       # achtergrond, screen capture
        elif self.currentstate == states.GameState.OverWorld:
            self.overworld.handle_view()

    def handle_multi_input(self):
        """
        Handelt de ingedrukt-houden muis en keyboard input af.
        """
        self.key_input = pygame.key.get_pressed()

        if self.currentstate == states.GameState.OverWorld:
            self.overworld.handle_multi_input(self.key_input, self.dt)

    def handle_single_input(self, event):
        """
        Handelt de muis en keyboard input af.
        :param event: pygame.event.get()
        """
        if event.type == pygame.KEYDOWN:
            print("Keyboard, key={}, unicode={}".format(event.key, event.unicode))

            if self.currentstate == states.GameState.MainMenu:
                menu_choice = self.mainmenu.handle_single_input(event)
                if event.key == pygame.K_F12:
                    self.show_debug ^= True                     # simple boolean swith
                elif menu_choice == menus.Main().NewGame:
                    self._main_menu_select_new_game()
                elif menu_choice == menus.Main().LoadGame:
                    self._main_menu_select_load_game()
                elif menu_choice == menus.Main().Options:
                    self._main_menu_select_options()
                elif menu_choice == menus.Main().ExitGame:
                    self._main_menu_select_exit_game()

            elif self.currentstate == states.GameState.OptionsMenu:
                menu_choice = self.optionsmenu.handle_single_input(event)
                if event.key == pygame.K_ESCAPE:
                    self._options_menu_select_back(with_esc=True)
                elif menu_choice == menus.Options().Back:
                    self._options_menu_select_back(with_esc=False)
                elif menu_choice == menus.Options().Music:
                    self._options_menu_select_music()
                elif menu_choice == menus.Options().Sound:
                    self._options_menu_select_sound()

            elif self.currentstate == states.GameState.PauseMenu:
                menu_choice = self.pausemenu.handle_single_input(event)
                if event.key == pygame.K_ESCAPE:
                    self._pause_menu_select_continue(with_esc=True)
                elif menu_choice == menus.Pause().ContinueGame:
                    self._pause_menu_select_continue(with_esc=False)
                elif menu_choice == menus.Pause().SaveGame:
                    self._pause_menu_select_save_game()
                elif menu_choice == menus.Pause().MainMenu:
                    self._show_main_menu()

            elif self.currentstate == states.GameState.OverWorld:
                self.overworld.handle_single_input(event)
                if event.key == pygame.K_ESCAPE:
                    self._show_pause_menu()
                if event.key == pygame.K_BACKSPACE:
                    self._kill_game()                           # todo, deze en de methode moeten uiteindelijk weg

    def _show_main_menu(self):
        if self.sound.current.get_sound() is not None:
            self.sound.current.fadeout(1000)
        self.pausemenu = None
        self.overworld = None
        self.state.clear()
        self.state.push(states.GameState.MainMenu)
        self.mainmenu = menu.GameMenu(self.screen, menus.Main(), True)
        self.sound.current.set_volume(1)
        self.sound.current.play(self.sound.mainmenu, -1, fade_ms=3000)

    def _main_menu_select_new_game(self):
        if self.sound.current.get_sound() is not None:
            self.sound.current.fadeout(1000)
        self.mainmenu = None
        self.state.pop(self.currentstate)
        self.state.push(states.GameState.OverWorld)
        self.overworld = overworld.OverWorld(self.screen)
        self.sound.current.set_volume(1)
        self.sound.current.play(self.sound.overworld, -1, fade_ms=3000)

    def _main_menu_select_load_game(self):
        self.loadsave = loadsave.Dialog()
        self.overworld = overworld.OverWorld(self.screen)       # laad de overworld alvast
        if self.loadsave.load(self) is None:
            self.overworld = None                               # toch niet
        else:                                                   # geef data mee aan de overworld
            self.sound.select.play()
            if self.sound.current.get_sound() is not None:
                self.sound.current.fadeout(1000)
            self.mainmenu = None
            self.state.pop(self.currentstate)
            self.state.push(states.GameState.OverWorld)
            self.sound.current.set_volume(1)
            self.sound.current.play(self.sound.overworld, -1, fade_ms=3000)
        pygame.event.clear()
        self.loadsave = None

    def _main_menu_select_options(self):
        self.state.push(states.GameState.OptionsMenu)
        self.optionsmenu = menu.GameMenu(self.screen, menus.Options(), True)

    def _main_menu_select_exit_game(self):
        if self.sound.current.get_sound() is not None:
            self.sound.current.fadeout(1000)
        self.running = False

    def _options_menu_select_music(self):
        settingview = self.optionsmenu.menu_texts[self.optionsmenu.cur_item]
        if self.optionsmenu.menu_items.music == 1:
            settingview.text = settingview.text.replace("On", "Off")
            self.optionsmenu.menu_items.music = 0
            self.optionsmenu.menu_items.write_cfg()
        else:
            settingview.text = settingview.text.replace("Off", "On")
            self.optionsmenu.menu_items.music = 1
            self.optionsmenu.menu_items.write_cfg()

    def _options_menu_select_sound(self):
        settingview = self.optionsmenu.menu_texts[self.optionsmenu.cur_item]
        if self.optionsmenu.menu_items.sound == 1:
            settingview.text = settingview.text.replace("On", "Off")
            self.optionsmenu.menu_items.sound = 0
            self.optionsmenu.menu_items.write_cfg()
        else:
            settingview.text = settingview.text.replace("Off", "On")
            self.optionsmenu.menu_items.sound = 1
            self.optionsmenu.menu_items.write_cfg()

    def _options_menu_select_back(self, with_esc):
        if with_esc:
            self.sound.select.play()
        self.state.pop(self.currentstate)
        self.optionsmenu = None

    def _show_pause_menu(self):
        self.sound.select.play()
        if self.sound.current.get_sound() is not None:
            self.sound.current.fadeout(1000)
        data = pygame.image.tostring(self.screen, 'RGBA')       # maak een screen capture
        self.scr_capt = pygame.image.frombuffer(data, self.screen.get_size(), 'RGBA')
        self.state.push(states.GameState.PauseMenu)
        self.pausemenu = menu.GameMenu(self.screen, menus.Pause(), False)

    def _pause_menu_select_save_game(self):
        self.loadsave = loadsave.Dialog()
        if self.loadsave.save(self) is not None:
            self.sound.select.play()
        pygame.event.clear()                                    # anders stapelen de geluiden zich op
        self.loadsave = None

    def _pause_menu_select_continue(self, with_esc):
        if with_esc:
            self.sound.select.play()                            # omdat escape in menu standaard geen geluid geeft
        self.state.pop(self.currentstate)
        self.pausemenu = None
        self.sound.current.set_volume(1)
        self.sound.current.play(self.sound.overworld, -1, fade_ms=3000)

    @staticmethod
    def _kill_game():
        import sys
        pygame.quit()
        sys.exit()
