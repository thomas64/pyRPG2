
"""
class: SettingsMenu
"""

from .basemenu import BaseMenu


class SettingsMenu(BaseMenu):
    """
    De settings items. Deze worden geladen uit een bestand en op aangepast.
    """
    def __init__(self, engine):
        super().__init__(engine)

        if engine.video.fullscreen:
            self.content.append('Full screen: On')
        else:
            self.content.append('Full screen: Off')
        if engine.audio.music:
            self.content.append('Music: On')
        else:
            self.content.append('Music: Off')
        if engine.audio.sound:
            self.content.append('Sound: On')
        else:
            self.content.append('Sound: Off')

        self.content.append('Back')

    def on_select(self, menu_item, title, animation, scr_capt, index):
        """
        Zie BaseMenu. Deze stelt de settingsweergave in.
        :param menu_item: zie BaseMenu
        :param title: zie BaseMenu
        :param animation: zie BaseMenu
        :param scr_capt: zie BaseMenu
        :param index: zie BaseMenu
        """
        if menu_item.text.startswith("Full screen:"):
            menu_item.flip_switch()
            self.engine.video.flip_fullscreen()
            self.engine.video.write_cfg()

        elif menu_item.text.startswith("Music:"):
            menu_item.flip_switch()             # hier wordt de weergave later aangepast
            self.engine.audio.flip_music()      # en de instelling zelf aangepast
            self.engine.audio.write_cfg()       # en weggeschreven

        elif menu_item.text.startswith("Sound:"):
            menu_item.flip_switch()
            self.engine.audio.flip_sound()
            self.engine.audio.write_cfg()

        elif menu_item.text == "Back":
            self.on_quit()
