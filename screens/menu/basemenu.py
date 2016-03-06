
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

    def on_select(self, key, state):
        """
        Als er in een menu iets geselecteerd wordt.
        :param key: een self.inside[key]
        :param state: het object Display, de visuele weergave van een menu
        """
        raise NotImplementedError

    def on_exit(self):
        """
        Als er een exit commando, bijvoorbeeld escape wordt gedaan.
        """
        raise NotImplementedError

    def on_delete(self, key, index):
        """
        Als er een delete commando gegeven wordt. Dit komt eigenlijk alleen voor bij LoadMenu.
        :param key: een self.inside[key]
        :param index: integer, welke menu item is geselecteerd
        """
        raise NotImplementedError
