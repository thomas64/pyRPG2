
"""
class: Item
class: Main
class: Options
class: Pause
"""

import collections


class Item(object):
    """
    Base class voor de verschillende menu's.
    Je kan er dan de lengte van bepalen, er doorheen loopen, en de attr van opvragen.
    """
    def __init__(self):
        self.inside = collections.OrderedDict()

    def __len__(self):
        return len(self.inside)

    def __iter__(self):
        return iter(self.inside.items())

    def __getattr__(self, key):
        return key


class Main(Item):
    """
    De mainmenu items.
    """
    def __init__(self):
        super().__init__()
        self.inside['NewGame'] = 'New Game'
        self.inside['LoadGame'] = 'Load Game'
        self.inside['Options'] = 'Options'
        self.inside['ExitGame'] = 'Exit'


class Options(Item):
    """
    De options items. Deze worden geladen uit een bestand en op aangepast.
    """
    def __init__(self, music=None, sound=None):
        super().__init__()

        if music == 1:
            self.inside['Music'] = 'Music: On'
        else:
            self.inside['Music'] = 'Music: Off'
        if sound == 1:
            self.inside['Sound'] = 'Sound: On'
        else:
            self.inside['Sound'] = 'Sound: Off'
        self.inside['Back'] = 'Back'


class Pause(Item):
    """
    De pausemenu items.
    """
    def __init__(self):
        super().__init__()
        self.inside['ContinueGame'] = 'Continue'
        self.inside['SaveGame'] = 'Save Game'
        self.inside['MainMenu'] = 'Main Menu'
