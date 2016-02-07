
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

# todo, descriptions van stats


class Stat(object):
    """
    ...
    """
    def __init__(self, name, raw, maximum, upgrade, quantity):
        self.NAME = name
        self.RAW = raw
        self.MAXIMUM = maximum     # maximum mogelijk, bijv 30
        self.UPGRADE = upgrade     # upgrade formule constante
        self.quantity = quantity   # standaard hoeveelheid op te waarderen stat (tot bijv 30)
        self.extra = 0             # wat geeft gear voor pos/neg extra
        self.total = quantity      # quantity + extra
        self.current = quantity    # gaat af wanneer er bijv schade is (sta, edu, lev)


class Level(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Level", "lev", 40, None, quantity)

    def next(self, totalxp):
        """
        ...
        :param totalxp:
        """
        if self.quantity >= self.MAXIMUM:
            return 1
        else:
            return int((250 / 3) * (2 * self.quantity ** 3 + 9 * self.quantity ** 2 + 13 * self.quantity + 6) - totalxp)


class Experience(object):
    """
    ...
    """
    def __init__(self, total):
        self.total = total
        self.remaining = 0


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
