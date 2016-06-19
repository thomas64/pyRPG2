
"""
class: Spell
"""

from database import SchoolType


SPRITEPATH = 'resources/sprites/icons/spells/spells.png'


class Spell(object):
    """
    ...
    """
    TRAININGSCOSTS = (200, 80, 120, 160, 200, 240, 280, 320, 360, 400, "Max")
    MAXIMUM = 10

    # todo, descriptions en docstrings

    def __init__(self, name, raw, srt, school, minimum_rank, upgrade, quantity):
        self.NAM = name
        self.RAW = raw
        self.SRT = srt
        self.ICON = SPRITEPATH
        self.SCL = school
        self.MIN = minimum_rank
        self.UPG = upgrade
        self.REQ = 0        # todo
        self.COST = 0       # todo
        self.qty = quantity

    def upgrade(self, quantity):
        """
        ...
        :param quantity:
        :return:
        """
        if self.qty >= self.MAXIMUM:
            return print("Spell is al aan de max, kan niet.")
        else:
            self.qty += quantity
            return print("Spell met 1 opgehoogd, gelukt.")

    def set_desc(self, text):
        """
        ...
        :param text:
        :return:
        """
        return (self.NAM,
                text,
                " ",
                "Min. Wizard Rank: {}".format(self.MIN),
                "Requires: {}".format(self.REQ),
                "Stamina Cost: {}".format(self.COST))


# Neutral ##############################################################################################################
class DispelNaming(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Dispel Naming", 'dis_nmg', 10, SchoolType.ntl, 2, 320, quantity)
        self.ROW = 0
        self.COL = 0
        self.DESC = self.set_desc("Text")


class DispelNecro(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Dispel Necro", 'dis_ncy', 20, SchoolType.ntl, 2, 320, quantity)
        self.ROW = 0
        self.COL = 0
        self.DESC = self.set_desc("This spell attempts to dispel any Necromantic spell currently in effect.")
        # "Requires: Gemstone"


class DispelStar(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Dispel Star", 'dis_str', 30, SchoolType.ntl, 2, 320, quantity)
        self.ROW = 0
        self.COL = 0
        self.DESC = self.set_desc("Text")


class Mirror(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Mirror", 'mir', 40, SchoolType.ntl, 6, 200, quantity)
        self.ROW = 0
        self.COL = 32
        self.DESC = self.set_desc("Text")


class VsElemental(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("vs. Elemental", 'vs_elm', 50, SchoolType.ntl, 1, 240, quantity)
        self.ROW = 0
        self.COL = 64
        self.DESC = self.set_desc("Text")


class VsNecromancy(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("vs. Necromancy", 'vs_ncy', 60, SchoolType.ntl, 1, 240, quantity)
        self.ROW = 0
        self.COL = 64
        self.DESC = self.set_desc("Increases the magic resistance to any Necromancy spell by 6 percent per Rank.")
        # "Requires: Gemstone"


class VsStar(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("vs. Star", 'vs_str', 70, SchoolType.ntl, 1, 240, quantity)
        self.ROW = 0
        self.COL = 64
        self.DESC = self.set_desc("Text")


# Elemental ############################################################################################################
class AirShield(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Air Shield", 'air_sld', 110, SchoolType.elm, 1, 320, quantity)
        self.ROW = 32
        self.COL = 0
        self.DESC = self.set_desc(
            "All friendly entities within the range of the spell add 1 per Rank to their Protection value.")
        # "Requires: Gemstone"


class Debilitation(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Debilitation", 'deb', 120, SchoolType.elm, 2, 320, quantity)
        self.ROW = 32
        self.COL = 32
        self.DESC = self.set_desc("Text")


class DragonFlames(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Dragon Flames", 'drg_flm', 130, SchoolType.elm, 2, 520, quantity)
        self.ROW = 32
        self.COL = 64
        self.DESC = self.set_desc("Text")


class Fireball(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Fireball", 'frb', 140, SchoolType.elm, 5, 400, quantity)
        self.ROW = 32
        self.COL = 96
        self.DESC = self.set_desc("Text")


class RemovePoison(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Remove Poison", 'rem_psn', 150, SchoolType.elm, 2, 80, quantity)
        self.ROW = 32
        self.COL = 128
        self.DESC = self.set_desc("Text")


class Strength(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Strength", 'str', 160, SchoolType.elm, 1, 160, quantity)
        self.ROW = 32
        self.COL = 160
        self.DESC = self.set_desc(
            "Target gains 2 Strength for each Rank of the spell. May only be cast once on each target.")
        # "Requires: Herb"


class Wind(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Wind", 'wnd', 170, SchoolType.elm, 4, 520, quantity)
        self.ROW = 32
        self.COL = 192
        self.DESC = self.set_desc("Text")


# Naming ###############################################################################################################
class Banishing(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Banishing", 'ban', 210, SchoolType.nmg, 4, 520, quantity)
        self.ROW = 64
        self.COL = 0
        self.DESC = self.set_desc("Text")


class Endurance(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Endurance", 'edu', 220, SchoolType.nmg, 2, 320, quantity)
        self.ROW = 64
        self.COL = 32
        self.DESC = self.set_desc(
            "Target gains 2 Endurance for each Rank of the spell. May only be cast once on each target.")
        # "Requires: Spice"


class SenseAura(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Sense Aura", 'sen_aur', 230, SchoolType.nmg, 3, 400, quantity)
        self.ROW = 64
        self.COL = 64
        self.DESC = self.set_desc(
            "Reveals a variety of information about the target: the higher the caster's rank in Sense Aura, "
            "the more information is revealed. May only be cast once on each target.")
        # "Requires: Herb"


class Teleportation(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Teleportation", 'tlp', 240, SchoolType.nmg, 8, 320, quantity)
        self.ROW = 64
        self.COL = 96
        self.DESC = self.set_desc("Text")


class Weakness(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Weakness", 'wks', 250, SchoolType.nmg, 2, 320, quantity)
        self.ROW = 64
        self.COL = 128
        self.DESC = self.set_desc(
            "Target loses 2 Endurance for each Rank of the spell. May only be cast once on each target.")
        # "Requires: Herb"


# Star #################################################################################################################
class SolarWrath(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Solar Wrath", 'sol_wrt', 310, SchoolType.str, 4, 80, quantity)
        self.ROW = 96
        self.COL = 0
        self.DESC = self.set_desc("Text")


class StellarGravity(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Stellar Gravity", 'stl_gty', 320, SchoolType.str, 2, 320, quantity)
        self.ROW = 96
        self.COL = 32
        self.DESC = self.set_desc("Text")


class WebOfStarlight(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Web of Starlight", 'wos', 330, SchoolType.str, 3, 400, quantity)
        self.ROW = 96
        self.COL = 64
        self.DESC = self.set_desc("Text")
