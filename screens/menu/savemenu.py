
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
            loadsave.Dialog(self.engine).save(menu_item.func)
            self.engine.gamestate.pop()
            push_object = screens.menu.manager.create_menu(statemachine.States.SaveMenu, self.engine,
                                                           scr_capt=scr_capt, select=index)
            self.engine.gamestate.push(push_object)
        else:
            push_object = screens.menu.inputbox.InputBox(self.engine, statemachine.States.SaveDialog)
            self.engine.gamestate.push(push_object)

            # todo, hoe krijg ik hier de input van inputbox terug?
