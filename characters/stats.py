
"""
class: Stat
class: Level
class: Experience
class: Intelligence
class: Willpower
class: Dexterity
class: Agility
class: Endurance
class: Strength
class: Stamina
"""

# todo, descriptions van stats, en docstrings


class Stat(object):
    """
    Stat baseclass voor stats en skills.
    """
    def __init__(self, name, raw, maximum, upgrade, quantity):
        self.NAM = name
        self.RAW = raw
        self.MAX = maximum          # maximum mogelijk, bijv 10 bij skill of 30 bij int
        self.UPG = upgrade          # upgrade formule constante
        self.qty = quantity         # standaard hoeveelheid op te waarderen stat (tot bijv 30)
        self.ext = 0                # extra: wat geeft gear voor pos/neg extra
        self.tot = quantity         # total: quantity + extra
        self.cur = quantity         # current: gaat af wanneer er bijv schade is (sta, edu, lev)


class Level(Stat):
    """
    Level. Heeft geen upgrade.
    """
    def __init__(self, quantity):
        super().__init__("Level", "lev", 40, None, quantity)

    def next(self, totalxp):
        """
        Dit betreft een formule van Anton, en verbeterd door Wolframe.
        :param totalxp:
        """
        if self.qty >= self.MAX:
            return 1
        else:
            return int((250 / 3) * (2 * self.qty ** 3 + 9 * self.qty ** 2 + 13 * self.qty + 6) - totalxp)


class Experience(object):
    """
    ...
    """
    def __init__(self, total):
        self.tot = total
        self.rem = 0        # remaining


class Intelligence(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Intelligence", "int", 30, 12, quantity)


class Willpower(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Willpower", "wil", 30, 12, quantity)


class Dexterity(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Dexterity", "dex", 30, 24, quantity)


class Agility(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Agility", "agi", 30, 24, quantity)


class Endurance(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Endurance", "edu", 40, 12, quantity)


class Strength(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Strength", "str", 30, 12, quantity)


class Stamina(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Stamina", "sta", 90, 4, quantity)
