
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

        if engine.video.fullscreen:
            self.inside['FullScreen'] = 'Full screen: On'
        else:
            self.inside['FullScreen'] = 'Full screen: Off'
        if engine.audio.music:
            self.inside['Music'] = 'Music: On'
        else:
            self.inside['Music'] = 'Music: Off'
        if engine.audio.sound:
            self.inside['Sound'] = 'Sound: On'
        else:
            self.inside['Sound'] = 'Sound: Off'

        self.inside['Back'] = 'Back'

    def on_select(self, menu_item, title, animation, scr_capt, index):
        """
        Zie BaseMenu. Deze stelt de settingsweergave in.
        :param menu_item: zie BaseMenu
        :param title: zie BaseMenu
        :param animation: zie BaseMenu
        :param scr_capt: zie BaseMenu
        :param index: zie BaseMenu
        """
        if menu_item.func == self.FullScreen:
            menu_item.flip_switch()
            self.engine.video.flip_fullscreen()
            self.engine.video.write_cfg()

        elif menu_item.func == self.Music:
            menu_item.flip_switch()             # hier wordt de weergave later aangepast
            self.engine.audio.flip_music()      # en de instelling zelf aangepast
            self.engine.audio.write_cfg()       # en weggeschreven

        elif menu_item.func == self.Sound:
            menu_item.flip_switch()
            self.engine.audio.flip_sound()
            self.engine.audio.write_cfg()

        elif menu_item.func == self.Back:
            self.on_exit()
