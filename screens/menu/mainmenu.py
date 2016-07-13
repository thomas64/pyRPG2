
"""
class: MainMenu
"""

from components import Map
from components import Transition
from constants import GameState
import data
import screens.overworld.display

from .basemenu import BaseMenu
import screens.menu


class MainMenu(BaseMenu):
    """
    De mainmenu items.
    """
    def __init__(self, engine):
        super().__init__(engine)

        self.content['NewGame'] = 'New Game'
        self.content['LoadGame'] = 'Load Game'
        self.content['Options'] = 'Options'
        self.content['ExitGame'] = 'Exit'

    def on_select(self, menu_item, title, animation, scr_capt, index):
        """
        Zie BaseMenu.
        :param menu_item: zie BaseMenu
        :param title: zie BaseMenu
        :param animation: zie BaseMenu
        :param scr_capt: zie BaseMenu
        :param index: zie BaseMenu
        """
        if menu_item.func == self.NewGame:
            self.engine.data = data.Data()
            self.engine.script.new_game()
            self.engine.current_map = Map(self.engine.data.map_name)
            push_object = screens.overworld.display.Display(self.engine)
            self.engine.gamestate.change(push_object)
            self.engine.gamestate.push(Transition(self.engine.gamestate))

        elif menu_item.func == self.LoadGame:
            push_object = screens.menu.create_menu(GameState.LoadMenu, self.engine)
            self.engine.gamestate.push(push_object)
            self.engine.gamestate.push(Transition(self.engine.gamestate))

        elif menu_item.func == self.Options:
            push_object = screens.menu.create_menu(GameState.OptionsMenu, self.engine,
                                                   title1=title, animation1=animation)
            self.engine.gamestate.push(push_object)

        elif menu_item.func == self.ExitGame:
            self.on_exit()

    def on_exit(self):
        """
        Zie BaseMenu. Stopt de engine.
        """
        self.engine.running = False
