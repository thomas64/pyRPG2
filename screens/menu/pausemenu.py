
"""
class: PauseMenu
"""

import loadsave
import screens.menu.basemenu


class PauseMenu(screens.menu.basemenu.BaseMenu):
    """
    De pausemenu items.
    """
    def __init__(self, engine):
        super().__init__(engine)

        self.inside['ContinueGame'] = 'Continue'
        self.inside['LoadGame'] = 'Load Game'
        self.inside['SaveGame'] = 'Save Game'
        self.inside['Options'] = 'Options'
        self.inside['MainMenu'] = 'Main Menu'

    def on_select(self, menu_item, title, animation, scr_capt):
        """
        Zie BaseMenu.
        :param menu_item: zie BaseMenu
        :param title: zie BaseMenu
        :param animation: zie BaseMenu
        :param scr_capt: zie BaseMenu
        """
        if menu_item.func == self.ContinueGame:
            self.on_exit()

        elif menu_item.func == self.LoadGame:
            push_object = screens.menu.manager.create_menu(screens.menu.manager.MenuItems.LoadMenu, self.engine,
                                                           scr_capt=scr_capt)
            self.engine.gamestate.push(push_object)

        elif menu_item.func == self.SaveGame:
            top_from_stack = self.engine.gamestate.peek()                   # dit is omdat hij de top van de stack
            self.engine.gamestate.pop()                                     # gebruikt om te saven, namelijk overworld,
            dialog = loadsave.Dialog(self.engine)
            if dialog.save():
                self.engine.audio.play_sound(self.engine.audio.select)
            self.engine.gamestate.push(top_from_stack)                      # die moet dus tijdelijk van de stack.
            import pygame
            pygame.event.clear()                                            # anders stapelen de geluiden zich op

        elif menu_item.func == self.Options:
            push_object = screens.menu.manager.create_menu(screens.menu.manager.MenuItems.OptionsMenu, self.engine,
                                                           scr_capt=scr_capt)
            self.engine.gamestate.push(push_object)

        elif menu_item.func == self.MainMenu:
            push_object = screens.menu.manager.create_menu(screens.menu.manager.MenuItems.MainMenu, self.engine,
                                                           select=-1)
            self.engine.gamestate.change(push_object)

    def on_exit(self):
        """
        Zie BaseMenu. Popt deze state.
        """
        self.engine.gamestate.pop()

    def on_delete(self, key, index, scr_capt):
        """
        Zie BaseMenu.
        :param key: zie BaseMenu
        :param index: zie BaseMenu
        :param scr_capt: zie BaseMenu
        """
        pass
