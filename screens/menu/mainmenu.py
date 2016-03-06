
"""
class: MainMenu
"""

import screens.menu.basemenu
import screens.overworld


class MainMenu(screens.menu.basemenu.BaseMenu):
    """
    De mainmenu items.
    """
    def __init__(self, engine):
        super().__init__(engine)

        self.inside['NewGame'] = 'New Game'
        self.inside['LoadGame'] = 'Load Game'
        self.inside['Options'] = 'Options'
        self.inside['ExitGame'] = 'Exit'

    def on_select(self, key, state):
        """
        Zie BaseMenu.
        :param key: zie BaseMenu
        :param state: zie BaseMenu
        """
        if key == self.NewGame:
            push_object = screens.overworld.Overworld(self.engine)
            self.engine.gamestate.push(push_object)

        elif key == self.LoadGame:
            push_object = screens.menu.create_menu(screens.menu.MenuItems.LoadMenu, self.engine)
            self.engine.gamestate.push(push_object)

        elif key == self.Options:
            push_object = screens.menu.create_menu(screens.menu.MenuItems.OptionsMenu, self.engine)
            self.engine.gamestate.push(push_object)

        elif key == self.ExitGame:
            self.engine.running = False

    def on_exit(self):
        """
        Zie BaseMenu. Stopt de engine.
        """
        self.engine.running = False

    def on_delete(self, key, index):
        """
        Zie BaseMenu.
        :param key: zie BaseMenu
        :param index: zie BaseMenu
        """
        pass
