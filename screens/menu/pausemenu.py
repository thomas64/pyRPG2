
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

        self.content = ['Continue',
                        'Load Game',
                        'Save Game',
                        'Settings',
                        'Main Menu']

    def on_select(self, menu_item, title, animation, scr_capt, index):
        """
        Zie BaseMenu.
        :param menu_item: zie BaseMenu
        :param title: zie BaseMenu
        :param animation: zie BaseMenu
        :param scr_capt: zie BaseMenu
        :param index: zie BaseMenu
        """
        if menu_item.text == "Continue":
            self.on_quit()

        elif menu_item.text == "Load Game":
            push_object = screens.menu.create_menu(GameState.LoadMenu, self.engine, scr_capt=scr_capt)
            self.engine.gamestate.push(push_object)

        elif menu_item.text == "Save Game":
            push_object = screens.menu.create_menu(GameState.SaveMenu, self.engine, scr_capt=scr_capt)
            self.engine.gamestate.push(push_object)

        elif menu_item.text == "Settings":
            push_object = screens.menu.create_menu(GameState.SettingsMenu, self.engine, scr_capt=scr_capt)
            self.engine.gamestate.push(push_object)

        elif menu_item.text == "Main Menu":
            push_object = screens.menu.create_menu(GameState.MainMenu, self.engine, select=-1)
            self.engine.gamestate.change(push_object, with_on_enter=False)
            self.engine.gamestate.push(Transition())
