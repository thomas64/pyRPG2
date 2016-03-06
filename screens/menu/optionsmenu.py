
"""
class: OptionsMenu
"""

import screens.menu


class OptionsMenu(screens.menu.BaseMenu):
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

    def on_select(self, key, state):
        """
        Zie BaseMenu. Deze stelt de settingsweergave in.
        :param key: zie BaseMenu
        :param state: zie BaseMenu
        """
        if key == self.Music:
            settingview = state.menu_texts[state.cur_item]                   # hier wordt de weergave
            settingview.flip_switch()                                        # later aangepast
            self.engine.audio.flip_music()                                   # en de instelling zelf aangepast
            self.engine.audio.write_cfg()                                    # en weggeschreven
        elif key == self.Sound:
            settingview = state.menu_texts[state.cur_item]
            settingview.flip_switch()
            self.engine.audio.flip_sound()
            self.engine.audio.write_cfg()
        elif key == self.Back:
            self.engine.gamestate.pop()

    def on_exit(self):
        """
        Zie BaseMenu. Popt deze state.
        """
        self.engine.gamestate.pop()

    def on_delete(self, key, index):
        """
        Zie BaseMenu.
        :param key: zie BaseMenu
        :param index: zie BaseMenu
        """
        pass
