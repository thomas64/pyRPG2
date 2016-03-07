
"""
class: LoadMenu
"""

import datetime
import os

import loadsave
import screens.menu.basemenu
import screens.menu.manager
import screens.overworld

SAVEPATH = 'savegame'


class LoadMenu(screens.menu.basemenu.BaseMenu):
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

    def on_select(self, menu_item, title, animation, scr_capt):
        """
        Zie BaseMenu.
        :param menu_item: zie BaseMenu
        :param title: zie BaseMenu
        :param animation: zie BaseMenu
        :param scr_capt: zie BaseMenu
        """
        if menu_item.func == self.Back:
            self.on_exit()
        else:
            self.engine.gamestate.change(screens.overworld.Overworld(self.engine))
            loadsave.Dialog(self.engine).load(menu_item.func)

    def on_exit(self):
        """
        Zie BaseMenu. Popt deze state.
        """
        self.engine.gamestate.pop()

    def on_delete(self, key, index, scr_capt):
        """
        Zie BaseMenu. Als er delete wordt gedrukt op niet de Back knop. Herlaad het hele object.
        :param key: zie BaseMenu
        :param index: zie BaseMenu
        :param scr_capt: zie BaseMenu
        """
        if key != self.Back:
            loadsave.Dialog(self.engine).delete(key)
            self.engine.gamestate.pop()

            push_object = screens.menu.manager.create_menu(screens.menu.manager.MenuItems.LoadMenu, self.engine,
                                                           scr_capt=scr_capt, select=index)
            self.engine.gamestate.push(push_object)
