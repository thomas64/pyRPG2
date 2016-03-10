
"""
class: BaseMenu
"""

import collections


class BaseMenu(object):
    """
    Base class voor de verschillende menu's.
    Je kan er dan de lengte van bepalen, er doorheen loopen, en de attr van opvragen.
    Enums zijn niet aan te passen.
    Gewone attribute strings staan niet op volgorde
    Vandaar gekozen voor een ordereddict.
    """
    def __init__(self, engine):
        self.inside = collections.OrderedDict()
        self.engine = engine

    def __len__(self):
        """
        Om de totale hoogte van alle items te kunnen berekenen, om het blok verticaal te kunnen centreren.
        """
        return len(self.inside)

    def __iter__(self):
        """
        Zodat de GameMenu class door alle enum items kan heen lopen om ze te kunnen projecteren.
        """
        return iter(self.inside.items())

    def __getattr__(self, key):
        """
        Om te controleren op een key zoals 'NewGame' of die gekozen wordt.
        """
        return key

    def on_select(self, menu_item, index, title, animation, scr_capt):
        """
        Als er in een menu iets geselecteerd wordt.
        :param menu_item: self.menu_texts[self.cur_item] uit Display. Dat is een key voor self.inside
        :param index: integer, welke menu item is geselecteerd
        :param title: de titel kan meegegeven worden
        :param animation: de animatie kan meegegeven worden
        :param scr_capt: een screencapture kan meegegeven worden
        """
        raise NotImplementedError

    def on_exit(self):
        """
        Als er een exit commando, bijvoorbeeld escape wordt gedaan.
        Popt de bovenste state.
        """
        self.engine.gamestate.pop()

    # noinspection PyMethodMayBeStatic
    def on_delete(self, menu_item, index, scr_capt):
        """
        Als er een delete commando gegeven wordt. Dit komt eigenlijk alleen voor bij LoadMenu.
        :param menu_item: self.menu_texts[self.cur_item] uit Display. Dat is een key voor self.inside
        :param index: integer, welke menu item is geselecteerd
        :param scr_capt: een screencapture
        """
        pass
