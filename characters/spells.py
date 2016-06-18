
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

    def __init__(self, name, raw, school, minimum_rank, upgrade, quantity):
        self.NAM = name
        self.RAW = raw
        self.ICON = SPRITEPATH
        self.SCL = school
        self.MIN = minimum_rank
        self.UPG = upgrade
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


# Neutral ##############################################################################################################
class DispelNaming(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Dispel Naming", 'dis_nmg', SchoolType.ntl, 2, 320, quantity)
        self.DESC = "Dispel Naming test"
        self.ROW = 0
        self.COL = 0


class DispelNecro(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Dispel Necro", 'dis_ncy', SchoolType.ntl, 2, 320, quantity)
        self.DESC = "Dispel Necro test"
        self.ROW = 0
        self.COL = 0


class DispelStar(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Dispel Star", 'dis_str', SchoolType.ntl, 2, 320, quantity)
        self.DESC = "Dispel Star test"
        self.ROW = 0
        self.COL = 0


class Mirror(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Mirror", 'mir', SchoolType.ntl, 6, 200, quantity)
        self.DESC = "Mirror test"
        self.ROW = 0
        self.COL = 32


class VsElemental(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("vs. Elemental", 'vs_elm', SchoolType.ntl, 1, 240, quantity)
        self.DESC = "vs. Elemental test"
        self.ROW = 0
        self.COL = 64


class VsNecromancy(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("vs. Necromancy", 'vs_ncy', SchoolType.ntl, 1, 240, quantity)
        self.DESC = "vs. Necromancy test"
        self.ROW = 0
        self.COL = 64


class VsStar(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("vs. Star", 'vs_str', SchoolType.ntl, 1, 240, quantity)
        self.DESC = "vs. Star test"
        self.ROW = 0
        self.COL = 64


# Elemental ############################################################################################################
class AirShield(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Air Shield", 'air_sld', SchoolType.elm, 1, 320, quantity)
        self.DESC = "Air Shield test"
        self.ROW = 32
        self.COL = 0


class Debilitation(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Debilitation", 'deb', SchoolType.elm, 2, 320, quantity)
        self.DESC = "Debilitation test"
        self.ROW = 32
        self.COL = 32


class DragonFlames(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Dragon Flames", 'drg_flm', SchoolType.elm, 2, 520, quantity)
        self.DESC = "Dragon Flames test"
        self.ROW = 32
        self.COL = 64


class Fireball(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Fireball", 'frb', SchoolType.elm, 5, 400, quantity)
        self.DESC = "Fireball test"
        self.ROW = 32
        self.COL = 96


class RemovePoison(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Remove Poison", 'rem_psn', SchoolType.elm, 2, 80, quantity)
        self.DESC = "Remove Poison test"
        self.ROW = 32
        self.COL = 128


class Strength(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Strength", 'str', SchoolType.elm, 1, 160, quantity)
        self.DESC = "Strength test"
        self.ROW = 32
        self.COL = 160


class Wind(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Wind", 'wnd', SchoolType.elm, 4, 520, quantity)
        self.DESC = "Wind test"
        self.ROW = 32
        self.COL = 192


# Naming ###############################################################################################################
class Banishing(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Banishing", 'ban', SchoolType.nmg, 4, 520, quantity)
        self.DESC = "Banishing test"
        self.ROW = 64
        self.COL = 0


class Endurance(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Endurance", 'edu', SchoolType.nmg, 2, 320, quantity)
        self.DESC = "Endurance test"
        self.ROW = 64
        self.COL = 32


class SenseAura(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Sense Aura", 'sen_aur', SchoolType.nmg, 3, 400, quantity)
        self.DESC = "Sense Aura test"
        self.ROW = 64
        self.COL = 64


class Teleportation(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Teleportation", 'tlp', SchoolType.nmg, 8, 320, quantity)
        self.DESC = "Teleportation test"
        self.ROW = 64
        self.COL = 96


class Weakness(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Weakness", 'wks', SchoolType.nmg, 2, 320, quantity)
        self.DESC = "Weakness test"
        self.ROW = 64
        self.COL = 128


# Star #################################################################################################################
class SolarWrath(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Solar Wrath", 'sol_wrt', SchoolType.str, 4, 80, quantity)
        self.DESC = "Solar Wrath test"
        self.ROW = 96
        self.COL = 0


class StellarGravity(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Stellar Gravity", 'stl_gty', SchoolType.str, 2, 320, quantity)
        self.DESC = "Stellar Gravity test"
        self.ROW = 96
        self.COL = 32


class WebOfStarlight(Spell):
    """
    ...
    """
    def __init__(self, quantity):
        super().__init__("Web of Starlight", 'wos', SchoolType.str, 3, 400, quantity)
        self.DESC = "Web of Starlight test"
        self.ROW = 96
        self.COL = 64
