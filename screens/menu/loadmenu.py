
"""
class: LoadMenu
"""

import datetime
import os

import loadsave
import screens.menu
import screens.overworld

SAVEPATH = 'savegame'


class LoadMenu(screens.menu.BaseMenu):
    """
    Hier worden alle bestanden van de savegame dir in een list gezet
    en weergegeven in de inside dict.
    """
    # todo, scrollbaar maken
    def __init__(self, engine):
        super().__init__(engine)

        files = []
        for (dirpath, dirnames, filenames) in os.walk(SAVEPATH):
            files.extend(filenames)
            break

        for file in files:
            timestamp = os.path.getmtime(os.path.join(SAVEPATH, file))
            timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            self.inside[file] = str(file)+" ["+str(timestamp)+"]"

        self.inside['Back'] = 'Back'

    def on_select(self, key, state):
        """
        Zie BaseMenu.
        :param key: zie BaseMenu
        :param state: zie BaseMenu
        """
        if key == self.Back:
            self.engine.gamestate.pop()
        else:
            self.engine.gamestate.push(screens.overworld.Overworld(self.engine))
            loadsave.Dialog(self.engine).load(key)

    def on_exit(self):
        """
        Zie BaseMenu. Popt deze state.
        """
        self.engine.gamestate.pop()

    def on_delete(self, key, index):
        """
        Zie BaseMenu. Als er delete wordt gedrukt op niet de Back knop.
        :param key: zie BaseMenu
        :param index: zie BaseMenu
        """
        if key != self.Back:
            loadsave.Dialog(self.engine).delete(key)
            self.engine.gamestate.pop()

            push_object = screens.menu.create_menu(screens.menu.MenuItems.LoadMenuFromMainMenu, self.engine, index)
            self.engine.gamestate.push(push_object)
