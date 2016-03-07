
"""
class: OptionsMenu
"""

import screens.menu.basemenu


class OptionsMenu(screens.menu.basemenu.BaseMenu):
    """
    De options items. Deze worden geladen uit een bestand en op aangepast.
    """
    def __init__(self, engine):
        super().__init__(engine)

        if engine.audio.music == 1:
            self.inside['Music'] = 'Music: On'
        else:
            self.inside['Music'] = 'Music: Off'
        if engine.audio.sound == 1:
            self.inside['Sound'] = 'Sound: On'
        else:
            self.inside['Sound'] = 'Sound: Off'

        self.inside['Back'] = 'Back'

    def on_select(self, menu_item, scr_capt):
        """
        Zie BaseMenu. Deze stelt de settingsweergave in.
        :param menu_item: zie BaseMenu
        :param scr_capt: zie BaseMenu
        """
        if menu_item.func == self.Music:
            settingview = menu_item                                          # hier wordt de weergave
            settingview.flip_switch()                                        # later aangepast
            self.engine.audio.flip_music()                                   # en de instelling zelf aangepast
            self.engine.audio.write_cfg()                                    # en weggeschreven
        elif menu_item.func == self.Sound:
            settingview = menu_item
            settingview.flip_switch()
            self.engine.audio.flip_sound()
            self.engine.audio.write_cfg()
        elif menu_item.func == self.Back:
            self.on_exit()

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
