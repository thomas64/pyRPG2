
"""
class: LoadMenu
"""

import datetime
import os

import loadsave
import screens.menu.basemenu
import screens.menu.manager
import screens.overworld
import statemachine

SAVEPATH = 'savegame'
MAXLOAD = 5


class LoadMenu(screens.menu.basemenu.BaseMenu):
    """
    Hier worden alle bestanden van de savegame dir in een list gezet
    en weergegeven in de inside dict.
    """
    def __init__(self, engine):
        super().__init__(engine)

        files = []
        for (dirpath, dirnames, filenames) in os.walk(SAVEPATH):
            files.extend(filenames)
            break

        index = 1
        for file in files:
            timestamp = os.path.getmtime(os.path.join(SAVEPATH, file))
            timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            self.inside[file] = "Slot {}:  {} [{}]".format(index, str(file), str(timestamp))
            index += 1

        while index <= MAXLOAD:
            self.inside['Slot'+str(index)] = "Slot {}:  ...".format(index)
            index += 1

        self.inside['Back'] = 'Back'

    def on_select(self, menu_item, index, title, animation, scr_capt):
        """
        Zie BaseMenu.
        :param menu_item: zie BaseMenu
        :param index: zie BaseMenu
        :param title: zie BaseMenu
        :param animation: zie BaseMenu
        :param scr_capt: zie BaseMenu
        """
        if menu_item.func == self.Back:
            self.on_exit()
        elif menu_item.func not in (self.Slot1, self.Slot2, self.Slot3, self.Slot4, self.Slot5):
            self.engine.gamestate.change(screens.overworld.Overworld(self.engine))
            loadsave.Dialog(self.engine).load(menu_item.func)

    def on_delete(self, menu_item, index, scr_capt):
        """
        Zie BaseMenu. Als er delete wordt gedrukt op niet de Back knop. Herlaad het hele object.
        :param menu_item: zie BaseMenu
        :param index: zie BaseMenu
        :param scr_capt: zie BaseMenu
        """
        if menu_item.func not in (self.Back, self.Slot1, self.Slot2, self.Slot3, self.Slot4, self.Slot5):
            loadsave.Dialog(self.engine).delete(menu_item.func)
            self.engine.gamestate.pop()

            push_object = screens.menu.manager.create_menu(statemachine.States.LoadMenu, self.engine,
                                                           scr_capt=scr_capt, select=index)
            self.engine.gamestate.push(push_object)
