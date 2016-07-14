
"""
class: BaseMenu
"""

from constants import SFX


class BaseMenu(object):
    """
    Base class voor de verschillende menu's.
    """
    def __init__(self, engine):
        self.content = list()
        self.engine = engine

    def on_select(self, menu_item, title, animation, scr_capt, index):
        """
        Als er in een menu iets geselecteerd wordt.
        :param menu_item: self.menu_texts[self.cur_item] uit Display. Dat is een Text() object
        :param title: de titel kan meegegeven worden
        :param animation: de animatie kan meegegeven worden
        :param scr_capt: een screencapture kan meegegeven worden
        :param index: integer, welke menu item is geselecteerd
        """
        raise NotImplementedError

    def on_exit(self):
        """
        Als er een exit commando, bijvoorbeeld escape wordt gedaan.
        Popt de bovenste state.
        """
        self.engine.gamestate.pop()

    def on_delete(self, menu_item, scr_capt, index):
        """
        Als er een delete commando gegeven wordt. Dit komt eigenlijk alleen voor bij LoadMenu.
        :param menu_item: self.menu_texts[self.cur_item] uit Display. Dat is een key voor self.inside
        :param scr_capt: een screencapture
        :param index: integer, welke menu item is geselecteerd
        """
        self.engine.audio.stop_sound(SFX.menu_select)
