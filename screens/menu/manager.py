
"""
...
"""

import pygame

import keys


class MenuManager(object):

    def handle_single_input(self, full_event):

        # todo, menu handler helemaal verbeteren
        # muziek later in laten komen?

        if self.menu_currentstate == states.MenuState.PauseMenu:
            if key_used == keys.SELECT:
                if menu_choice == self.menu_content.ContinueGame:
                    self._pause_menu_select_continue()
                elif menu_choice == self.menu_content.LoadGame:
                    self._menu_select_load_game()
                elif menu_choice == self.menu_content.SaveGame:
                    pass
                elif menu_choice == self.menu_content.Options:
                    self._menu_select_options()
                elif menu_choice == self.menu_content.MainMenu:
                    self._pause_menu_select_main_menu()
            if key_used == keys.EXIT:
                self._pause_menu_select_continue()

    def _pause_menu_select_continue(self):
        self.scr_capt = None
        self.menu = None
        self.menu_statemachine.pop(self.menu_currentstate)
        self.engine.statemachine.pop(self.engine.currentstate)

    def _pause_menu_select_main_menu(self):
        self.scr_capt = None
        self.menu = None
        self.menu_statemachine.change(states.MenuState.MainMenu)
        self.engine.statemachine.change(states.GameState.Menu)
        self.last_item = -1

########################################################################################################################

    def _pause_menu_select_save_game(self):
        dialog = screens.loadsave.Dialog(self)
        if dialog.save():
            self.audio.play_sound(self.audio.select)
        pygame.event.clear()                                                  # anders stapelen de geluiden zich op
