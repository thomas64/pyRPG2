
"""
class: SaveMenu
"""

import loadsave
import screens.menu.inputbox
import screens.menu.loadmenu
import statemachine


class SaveMenu(screens.menu.loadmenu.LoadMenu):
    """
    Heeft LoadMenu als base class.
    """
    def on_select(self, menu_item, title, animation, scr_capt, index):
        """
        Zie BaseMenu.
        :param menu_item: zie BaseMenu
        :param title: zie BaseMenu
        :param animation: zie BaseMenu
        :param scr_capt: zie BaseMenu
        :param index: zie BaseMenu
        """
        if menu_item.func == self.Back:
            self.on_exit()
        elif menu_item.func not in (self.Slot1, self.Slot2, self.Slot3, self.Slot4, self.Slot5):
            loadsave.Dialog(self.engine).save(menu_item.func)
            self._reload(scr_capt, index)
        else:
            filename = screens.menu.inputbox.InputBox(self.engine.screen).input_loop()
            if filename:
                loadsave.Dialog(self.engine).save(filename)
                self._reload(scr_capt, index)

    def _reload(self, scr_capt, index):
        self.engine.gamestate.pop()
        push_object = screens.menu.manager.create_menu(statemachine.States.SaveMenu, self.engine,
                                                       scr_capt=scr_capt, select=index)
        self.engine.gamestate.push(push_object)
