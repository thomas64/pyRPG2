
"""
class: PauseMenu
"""

import screens.menu.basemenu
import statemachine


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

    def on_select(self, menu_item, index, title, animation, scr_capt):
        """
        Zie BaseMenu.
        :param menu_item: zie BaseMenu
        :param index: zie BaseMenu
        :param title: zie BaseMenu
        :param animation: zie BaseMenu
        :param scr_capt: zie BaseMenu
        """
        if menu_item.func == self.ContinueGame:
            self.on_exit()

        elif menu_item.func == self.LoadGame:
            push_object = screens.menu.manager.create_menu(statemachine.States.LoadMenu, self.engine,
                                                           scr_capt=scr_capt)
            self.engine.gamestate.push(push_object)

        elif menu_item.func == self.SaveGame:
            push_object = screens.menu.manager.create_menu(statemachine.States.SaveMenu, self.engine,
                                                           scr_capt=scr_capt)
            self.engine.gamestate.push(push_object)

        elif menu_item.func == self.Options:
            push_object = screens.menu.manager.create_menu(statemachine.States.OptionsMenu, self.engine,
                                                           scr_capt=scr_capt)
            self.engine.gamestate.push(push_object)

        elif menu_item.func == self.MainMenu:
            push_object = screens.menu.manager.create_menu(statemachine.States.MainMenu, self.engine,
                                                           select=-1)
            self.engine.gamestate.change(push_object)
