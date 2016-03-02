
"""
...
"""

import pygame

import screens.menu.content
import screens.menu.display
# import screens.loadsave
# import screens.overworld
import states


class MenuManager(object):
    """
    ...
    """
    def __init__(self, engine):
        self.engine = engine
        self.menu_statemachine = states.StateMachine()
        self.menu_currentstate = None
        self.menu = None
        self.menu_content = None
        self.scr_capt = None
        self.cur_item = None        # todo, deze gaan gebruiken om de juiste menu selectie te doen.

    def open_menu(self, new_state):
        """

        :param new_state:
        """
        self.engine.statemachine.push(states.GameState.Menu)
        self.menu_statemachine.push(new_state)

    def loop(self):
        """
        ...
        """
        self.menu_currentstate = self.menu_statemachine.peek()

        if self.menu_currentstate == states.MenuState.MainMenu:
            if self.menu is None:
                cur_item = 0
                self.menu_content = screens.menu.content.MainMenu()
                self.menu = screens.menu.display.Display(self.engine.screen, self.engine.audio,
                                                         self.menu_content, True, True, cur_item)

        elif self.menu_currentstate == states.MenuState.LoadMenu:
            if self.menu is None:
                cur_item = -1
                self.menu_content = screens.menu.content.LoadMenu()
                self.menu = screens.menu.display.Display(self.engine.screen, self.engine.audio,
                                                         self.menu_content, False, False, cur_item)

        elif self.menu_currentstate == states.MenuState.SaveMenu:
            if self.menu is None:
                pass

        elif self.menu_currentstate == states.MenuState.OptionsMenu:
            if self.menu is None:
                cur_item = -1
                # hier wordt de weergave van options gekozen
                self.menu_content = screens.menu.content.OptionsMenu(self.engine.audio.music, self.engine.audio.sound)
                self.menu = screens.menu.display.Display(self.engine.screen, self.engine.audio,
                                                         self.menu_content, True, True, cur_item)

        elif self.menu_currentstate == states.MenuState.PauseMenu:
            if self.menu is None:
                scr_data = pygame.image.tostring(self.engine.screen, 'RGBA')                 # maak een screen capture
                self.scr_capt = pygame.image.frombuffer(scr_data, self.engine.screen.get_size(), 'RGBA').convert()
                self.menu_content = screens.menu.content.PauseMenu()
                self.menu = screens.menu.display.Display(self.engine.screen, self.engine.audio,
                                                         self.menu_content, False, False)

    def handle_view(self, dt):
        """
        ...
        :param dt:
        """
        self.menu.handle_view(dt, self.scr_capt)

    def handle_menu_input(self, full_event):

        # todo, menu handler helemaal verbeteren
        # muziek later in laten komen?

        """

        :param full_event:
        :return:
        """

        menu_choice, key_used = self.menu.handle_single_input(full_event)

        if self.menu_currentstate == states.MenuState.MainMenu:
            if key_used == 'enter':
                if menu_choice == self.menu_content.NewGame:
                    self._main_menu_select_new_game()
                elif menu_choice == self.menu_content.LoadGame:
                    self._main_menu_select_load_game()
                elif menu_choice == self.menu_content.Options:
                    self._main_menu_select_options()
                elif menu_choice == self.menu_content.ExitGame:
                    self._main_menu_select_exit_game()
            elif key_used == 'escape':
                self._main_menu_select_exit_game()

        elif self.menu_currentstate == states.MenuState.LoadMenu:
            if key_used == 'enter':
                if menu_choice == self.menu_content.Back:
                    self._load_game_menu_select_back()
                else:
                    self._load_game_menu_select_savefile(menu_choice)
            elif key_used == 'escape':
                self._load_game_menu_select_back()
            elif key_used == 'delete':
                if menu_choice != self.menu_content.Back:
                    self._load_game_menu_delete_savefile(menu_choice)

        elif self.menu_currentstate == states.MenuState.SaveMenu:
            pass

        elif self.menu_currentstate == states.MenuState.OptionsMenu:
            if key_used == 'enter':
                if menu_choice == self.menu_content.Music:              # .Music geeft de key "Music"
                    self._options_menu_select_music()
                elif menu_choice == self.menu_content.Sound:
                    self._options_menu_select_sound()
                elif menu_choice == self.menu_content.Back:
                    self._options_menu_select_back()
            if key_used == 'escape':
                self._options_menu_select_back()

        elif self.menu_currentstate == states.MenuState.PauseMenu:
            if key_used == 'enter':
                if menu_choice == self.menu_content.ContinueGame:
                    self._pause_menu_select_continue()
                elif menu_choice == self.menu_content.SaveGame:
                    self._pause_menu_select_save_game()
                elif menu_choice == self.menu_content.MainMenu:
                    self._pause_menu_select_main_menu()
            if key_used == 'escape':
                self._pause_menu_select_continue()

    def _main_menu_select_new_game(self):
        self.menu = None
        self.menu_statemachine.clear()
        self.engine.statemachine.change(states.GameState.Overworld)

    def _main_menu_select_options(self):
        self.menu = None
        self.menu_statemachine.push(states.MenuState.OptionsMenu)

########################################################################################################################

    def _show_main_menu(self, from_state):
        cur_item = 0
        if from_state is None:
            self.statemachine.push(states.GameState.MainMenu)
        elif from_state == states.GameState.LoadMenu:
            # todo, geen magische nummers, maar get de index uit screens.menu.content.MainMenu()
            cur_item = 1
        elif from_state == states.GameState.OptionsMenu:
            cur_item = 2
        elif from_state == states.GameState.PauseMenu:
            self.scr_capt = None
            self.overworld = None
            self.statemachine.change(states.GameState.MainMenu)

        menu_items = screens.menu.content.MainMenu()
        self.menu = screens.menu.display.Display(self.screen, self.audio, menu_items, True, True, cur_item)

    def _main_menu_select_load_game(self):
        self._show_load_game_menu()

    def _main_menu_select_exit_game(self):
        self.running = False

    def _show_load_game_menu(self):
        self.statemachine.push(states.GameState.LoadMenu)
        cur_item = -1
        menu_items = screens.menu.content.LoadMenu()
        self.menu = screens.menu.display.Display(self.screen, self.audio, menu_items, False, False, cur_item)

    def _load_game_menu_select_back(self):
        self.statemachine.pop(self.currentstate)
        self._show_main_menu(self.currentstate)

    def _load_game_menu_select_savefile(self, savefile):
        dialog = screens.loadsave.Dialog(self)
        self.overworld = screens.overworld.Overworld(self)                    # laad de overworld alvast
        if dialog.load(savefile) is None:
            self.overworld = None                                             # toch niet
        else:                                                                 # geef dan data mee aan de overworld
            self.audio.play_sound(self.audio.select)
            self.menu = None
            self.statemachine.change(states.GameState.Overworld)

    def _load_game_menu_delete_savefile(self, savefile):
        dialog = screens.loadsave.Dialog(self)
        dialog.delete(savefile)
        self.statemachine.pop(self.currentstate)
        self._show_load_game_menu()

    def _show_options_menu(self):
        self.statemachine.push(states.GameState.OptionsMenu)
        cur_item = -1
        # hier wordt de weergave van options gekozen
        menu_items = screens.menu.content.OptionsMenu(self.audio.music, self.audio.sound)
        self.menu = screens.menu.display.Display(self.screen, self.audio, menu_items, True, True, cur_item)

    def _options_menu_select_music(self):
        # todo, ipv switch net zoals delete savefile doen? volledig opnieuw laden?
        settingview = self.menu.menu_texts[self.menu.cur_item]                # hier wordt de weergave
        settingview.flip_switch()                                             # later aangepast
        self.audio.flip_music()                                               # en de instelling zelf aangepast
        self.audio.write_cfg()                                                # en weggeschreven

    def _options_menu_select_sound(self):
        settingview = self.menu.menu_texts[self.menu.cur_item]
        settingview.flip_switch()
        self.audio.flip_sound()
        self.audio.write_cfg()

    def _options_menu_select_back(self):
        self.statemachine.pop(self.currentstate)
        self._show_main_menu(self.currentstate)

    def _show_pause_menu(self):
        scr_data = pygame.image.tostring(self.screen, 'RGBA')                 # maak een screen capture
        self.scr_capt = pygame.image.frombuffer(scr_data, self.screen.get_size(), 'RGBA').convert()
        self.statemachine.push(states.GameState.PauseMenu)
        menu_items = screens.menu.content.PauseMenu()
        self.menu = screens.menu.display.Display(self.screen, self.audio, menu_items, False, False)

    def _pause_menu_select_continue(self):
        self.menu = None
        self.scr_capt = None
        self.statemachine.pop(self.currentstate)

    def _pause_menu_select_save_game(self):
        dialog = screens.loadsave.Dialog(self)
        if dialog.save():
            self.audio.play_sound(self.audio.select)
        pygame.event.clear()                                                  # anders stapelen de geluiden zich op

    def _pause_menu_select_main_menu(self):
        self._show_main_menu(self.currentstate)
