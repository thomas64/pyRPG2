
"""
class: MenuItem
class: MainMenu
class: OptionsMenu
class: PauseMenu
"""

import collections
import os
import datetime

SAVEPATH = 'savegame'


class MenuItem(object):
    """
    Base class voor de verschillende menu's.
    Je kan er dan de lengte van bepalen, er doorheen loopen, en de attr van opvragen.
    Enums zijn niet aan te passen.
    Gewone attribute strings staan niet op volgorde
    Vandaar gekozen voor een ordereddict.
    """
    def __init__(self):
        self.inside = collections.OrderedDict()

    def __len__(self):                      # om de totale hoogte van alle items te kunnen berekenen, om het blok
        return len(self.inside)             # verticaal te kunnen centreren.

    def __iter__(self):                     # zodat de GameMenu class door alle enum items kan heen lopen
        return iter(self.inside.items())    # om ze te kunnen projecteren.

    def __getattr__(self, key):             # om te controleren op een key zoals 'NewGame' of die gekozen wordt
        return key


class MainMenu(MenuItem):
    """
    De mainmenu items.
    """
    def __init__(self):
        super().__init__()
        self.inside['NewGame'] = 'New Game'
        self.inside['LoadGame'] = 'Load Game'
        self.inside['Options'] = 'Options'
        self.inside['ExitGame'] = 'Exit'


class OptionsMenu(MenuItem):
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


class LoadMenu(MenuItem):
    """
    Hier worden alle bestanden van de savegame dir in een list gezet
    en weergegeven in de inside dict.
    """
    # todo, scrollbaar maken
    def __init__(self):
        super().__init__()

        files = []
        for (dirpath, dirnames, filenames) in os.walk(SAVEPATH):
            files.extend(filenames)
            break

        for file in files:
            timestamp = os.path.getmtime(os.path.join(SAVEPATH, file))
            timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            self.inside[file] = str(file)+" ["+str(timestamp)+"]"

        self.inside['Back'] = 'Back'


class PauseMenu(MenuItem):
    """
    De pausemenu items.
    """
    def __init__(self):
        super().__init__()
        self.inside['ContinueGame'] = 'Continue'
        self.inside['LoadGame'] = 'Load Game'
        self.inside['SaveGame'] = 'Save Game'
        self.inside['Options'] = 'Options'
        self.inside['MainMenu'] = 'Main Menu'
