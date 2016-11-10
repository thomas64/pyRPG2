
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

from constants import StatType

# todo, descriptions van stats, en docstrings


class Stat(object):
    """
    Stat baseclass voor stats.
    """
    def __init__(self, name, raw, maximum, upgrade, quantity):
        self.NAM = name
        self.RAW = raw
        self.MAX = maximum              # maximum mogelijk, bijv 30 bij int of 40 bij edu
        self.UPG = upgrade              # upgrade formule constante
        self.qty = quantity             # standaard hoeveelheid op te waarderen stat (tot bijv 30)
        self.ext = 0                    # extra: wat geeft equipment item voor pos/neg extra

    @property
    def xp_cost(self):
        """
        ...
        :return:
        """
        return round(self.UPG * ((self.qty + 1)**2))

    def is_able_to_upgrade(self, xp_amount):
        """
        ...
        :return:
        """
        if self.qty >= self.MAX:
            return False, ["You cannot train {} any further.".format(self.NAM)]

        elif self.xp_cost > xp_amount:
            return False, ["You need {} more XP to".format(self.xp_cost - xp_amount),
                           "train {}.".format(self.NAM)]
        else:
            return True, None

    def upgrade(self):
        """
        ...
        :return:
        """
        self.qty += 1

    @property
    def tot(self):
        """
        self.tot = self.qty + self.ext
        total: quantity + extra
        """
        total = self.qty + self.ext
        if total < 1:                   # het origineel uit vb.net is < 0, klopt dat?
            total = 1
        return total


class Level(Stat):
    """
    Level. Heeft geen upgrade.
    """
    def __init__(self, quantity):
        super().__init__("Level", "lev", 40, None, quantity)
        self.cur = quantity             # current: gaat af wanneer er bijv schade is (sta, edu, lev)

    def next(self, totalxp):
        """
        Dit betreft een formule van Anton, en verbeterd door Wolframe.
        :param totalxp: dit is experience.tot
        """
        if self.qty >= self.MAX:
            return 1
        else:
            # return int((250 / 3) * (2 * self.qty ** 3 + 9 * self.qty ** 2 + 13 * self.qty + 6) - totalxp)
            # de nieuwe lage xp berekening
            return int((5/6) * (2*self.qty + 3) * (self.qty**2 + 3*self.qty + 2) - totalxp)


class Experience(object):
    """
    Erft niet van Stat. Hier wordt eenmalig de eerste keer bij het aanmaken van
    de hero de experience berekend aan de hand van het gegeven level.
    """
    def __init__(self, level):
        self.tot = int((5/6) * (2*level + 1) * (level**2 + level))
        self.rem = 0                    # remaining


class Intelligence(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__(StatType.int.value, StatType.int.name, 30, 0.12, quantity)
        self.DESC = ("Dit is een ",
                     "test.",
                     "intelligence",
                     " ",
                     "XP Cost: {}".format(self.xp_cost))


class Willpower(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__(StatType.wil.value, StatType.wil.name, 30, 0.12, quantity)
        self.DESC = ("Dit is een ",
                     "test.",
                     "willpower")


class Dexterity(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__(StatType.dex.value, StatType.dex.name, 30, 0.24, quantity)
        self.DESC = ("Dit is een ",
                     "test.",
                     "Dexterity")


class Agility(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__(StatType.agi.value, StatType.agi.name, 30, 0.24, quantity)
        self.DESC = ("Dit is een ",
                     "test.",
                     "Agility")


class Endurance(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__(StatType.edu.value, StatType.edu.name, 40, 0.12, quantity)
        self.cur = quantity             # current: gaat af wanneer er bijv schade is (sta, edu, lev)
        self.DESC = ("Dit is een ",
                     "test.",
                     "Endurance")

    def upgrade(self):
        """
        ...
        :return:
        """
        self.qty += 1
        self.cur += 1


class Strength(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__(StatType.str.value, StatType.str.name, 30, 0.12, quantity)
        self.DESC = ("Dit is een ",
                     "test.",
                     "Strength")


class Stamina(Stat):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__(StatType.sta.value, StatType.sta.name, 90, 0.04, quantity)
        self.cur = quantity             # current: gaat af wanneer er bijv schade is (sta, edu, lev)
        self.DESC = ("Dit is een ",
                     "test.",
                     "Stamina")

    def upgrade(self):
        """
        ...
        :return:
        """
        self.qty += 1
        self.cur += 1
