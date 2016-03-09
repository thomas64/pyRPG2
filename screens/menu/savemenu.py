
"""
class: SaveMenu
"""

import screens.menu.loadmenu


class SaveMenu(screens.menu.loadmenu.LoadMenu):
    """
    ...
    """
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
        elif menu_item.func == self.Slot2:
            pass
