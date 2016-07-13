
"""
class: PauseMenu
"""

from components import Transition
from constants import GameState

from .basemenu import BaseMenu
import screens.menu


class PauseMenu(BaseMenu):
    """
    De pausemenu items.
    """
    def __init__(self, engine):
        super().__init__(engine)

        self.content['ContinueGame'] = 'Continue'
        self.content['LoadGame'] = 'Load Game'
        self.content['SaveGame'] = 'Save Game'
        self.content['Options'] = 'Options'
        self.content['MainMenu'] = 'Main Menu'

    def on_select(self, menu_item, title, animation, scr_capt, index):
        """
        Zie BaseMenu.
        :param menu_item: zie BaseMenu
        :param title: zie BaseMenu
        :param animation: zie BaseMenu
        :param scr_capt: zie BaseMenu
        :param index: zie BaseMenu
        """
        if menu_item.func == self.ContinueGame:
            self.on_exit()

        elif menu_item.func == self.LoadGame:
            push_object = screens.menu.create_menu(GameState.LoadMenu, self.engine, scr_capt=scr_capt)
            self.engine.gamestate.push(push_object)

        elif menu_item.func == self.SaveGame:
            push_object = screens.menu.create_menu(GameState.SaveMenu, self.engine, scr_capt=scr_capt)
            self.engine.gamestate.push(push_object)

        elif menu_item.func == self.Options:
            push_object = screens.menu.create_menu(GameState.OptionsMenu, self.engine, scr_capt=scr_capt)
            self.engine.gamestate.push(push_object)

        elif menu_item.func == self.MainMenu:
            push_object = screens.menu.create_menu(GameState.MainMenu, self.engine, select=-1)
            self.engine.gamestate.change(push_object)
            self.engine.gamestate.push(Transition(self.engine.gamestate))
