
"""
class: MainMenu
"""

from components import MessageBox
from components import Transition
from constants import GameState
from data import Data
from screens import Overworld
from script import Script

from .basemenu import BaseMenu
import screens.menu


class MainMenu(BaseMenu):
    """
    De mainmenu items.
    """
    def __init__(self, engine):
        super().__init__(engine)

        self.content = ['New Game',
                        'Load Game',
                        'Settings',
                        'Exit']

    def on_select(self, menu_item, title, animation, scr_capt, index):
        """
        Zie BaseMenu.
        :param menu_item: zie BaseMenu
        :param title: zie BaseMenu
        :param animation: zie BaseMenu
        :param scr_capt: zie BaseMenu
        :param index: zie BaseMenu
        """
        if menu_item.text == "New Game":
            self.engine.wait_for_transition_before_loading_music = True
            self.engine.audio.fade_bg_music()
            self.engine.data = Data()
            Script.new_game(self.engine.data)
            push_object = Overworld(self.engine)
            self.engine.gamestate.change(push_object)
            self.engine.gamestate.push(Transition(self.engine.gamestate))
            self.engine.gamestate.push(MessageBox(self.engine.gamestate, self.engine.audio, Script.intro_text(),
                                                  scr_capt=False, sound=None))
            self.engine.gamestate.push(Transition(self.engine.gamestate))
            self.engine.wait_for_transition_before_loading_music = False
            self.engine.try_to_load_music = True

        elif menu_item.text == "Load Game":
            push_object = screens.menu.create_menu(GameState.LoadMenu, self.engine)
            self.engine.gamestate.push(push_object)
            self.engine.gamestate.push(Transition(self.engine.gamestate))

        elif menu_item.text == "Settings":
            push_object = screens.menu.create_menu(GameState.SettingsMenu, self.engine,
                                                   title1=title, animation1=animation)
            self.engine.gamestate.push(push_object)

        elif menu_item.text == "Exit":
            self.on_quit()

    def on_quit(self):
        """
        Zie BaseMenu. Stopt de engine.
        """
        self.engine.running = False
