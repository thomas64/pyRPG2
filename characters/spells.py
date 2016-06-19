
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
    ICON = SPRITEPATH

    # todo, descriptions en docstrings

    def __init__(self):
        self.NAM = None
        self.RAW = None
        self.SCL = None
        self.MIN = None
        self.UPG = None
        self.REQ = None        # todo
        self.COST = None       # todo
        self.qty = None

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
        return ("{} ({})".format(self.NAM, self.SCL.value),
                text,
                " ",
                "Min. Wizard Rank: {}".format(self.MIN),
                "Requires: {}".format(self.REQ),
                "Stamina Cost: {}".format(self.COST))


# Neutral ##############################################################################################################
class DispelNaming(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Dispel Naming"
        self.RAW = 'dis_nmg'
        self.SRT = 10
        self.SCL = SchoolType.ntl
        self.MIN = 2
        self.UPG = 320
        self.qty = quantity
        self.COL = 224
        self.ROW = 32
        self.DESC = self.set_desc("Text")


class DispelNecro(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Dispel Necro"
        self.RAW = 'dis_ncy'
        self.SRT = 20
        self.SCL = SchoolType.ntl
        self.MIN = 2
        self.UPG = 320
        self.qty = quantity
        self.COL = 224
        self.ROW = 32
        self.DESC = self.set_desc("This spell attempts to dispel any Necromantic spell currently in effect.")
        # "Requires: Gemstone"


class DispelStar(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Dispel Star"
        self.RAW = 'dis_str'
        self.SRT = 30
        self.SCL = SchoolType.ntl
        self.MIN = 2
        self.UPG = 320
        self.qty = quantity
        self.COL = 224
        self.ROW = 32
        self.DESC = self.set_desc("Text")


class Mirror(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Mirror"
        self.RAW = 'mir'
        self.SRT = 40
        self.SCL = SchoolType.ntl
        self.MIN = 6
        self.UPG = 200
        self.qty = quantity
        self.COL = 352
        self.ROW = 96
        self.DESC = self.set_desc(
            "Creates a shield that provides total resistance against the next incoming attack spells.")
        # Gemstone


class VsElemental(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "vs. Elemental"
        self.RAW = 'vs_elm'
        self.SRT = 50
        self.SCL = SchoolType.ntl
        self.MIN = 1
        self.UPG = 240
        self.qty = quantity
        self.COL = 256
        self.ROW = 32
        self.DESC = self.set_desc("Increases the magic resistance to any Elemental Magic spell by 6 percent per Rank.")
        # Gemstone


class VsNaming(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "vs. Naming"
        self.RAW = 'vs_nmg'
        self.SRT = 60
        self.SCL = SchoolType.ntl
        self.MIN = 1
        self.UPG = 240
        self.qty = quantity
        self.COL = 256
        self.ROW = 32
        self.DESC = self.set_desc("Increases the magic resistance to any Naming Magic spell by 6 percent per Rank.")
        # Gemstone


class VsNecromancy(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "vs. Necromancy"
        self.RAW = 'vs_ncy'
        self.SRT = 70
        self.SCL = SchoolType.ntl
        self.MIN = 1
        self.UPG = 240
        self.qty = quantity
        self.COL = 256
        self.ROW = 32
        self.DESC = self.set_desc("Increases the magic resistance to any Necromancy spell by 6 percent per Rank.")
        # "Requires: Gemstone"


class VsStar(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "vs. Star"
        self.RAW = 'vs_str'
        self.SRT = 80
        self.SCL = SchoolType.ntl
        self.MIN = 1
        self.UPG = 240
        self.qty = quantity
        self.COL = 256
        self.ROW = 32
        self.DESC = self.set_desc("Increases the magic resistance to any Star Magic spell by 6 percent per Rank.")
        # Gemstone


# Elemental ############################################################################################################
class AirShield(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Air Shield"
        self.RAW = 'air_sld'
        self.SRT = 110
        self.SCL = SchoolType.elm
        self.MIN = 1
        self.UPG = 320
        self.qty = quantity
        self.COL = 352
        self.ROW = 128
        self.DESC = self.set_desc(
            "All friendly entities within the range of the spell add 1 per Rank to their Protection value.")
        # "Requires: Gemstone"


class Debilitation(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Debilitation"
        self.RAW = 'deb'
        self.SRT = 120
        self.SCL = SchoolType.elm
        self.MIN = 2
        self.UPG = 320
        self.qty = quantity
        self.COL = 128
        self.ROW = 128
        self.DESC = self.set_desc("Text")


class DragonFlames(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Dragon Flames"
        self.RAW = 'drg_flm'
        self.SRT = 130
        self.SCL = SchoolType.elm
        self.MIN = 2
        self.UPG = 520
        self.qty = quantity
        self.COL = 32
        self.ROW = 0
        self.DESC = self.set_desc(
            "The target(s) of this spell are attacked by wicked dragon flames emanating from the caster.")
        # Gemstone


class Fireball(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Fireball"
        self.RAW = 'frb'
        self.SRT = 140
        self.SCL = SchoolType.elm
        self.MIN = 5
        self.UPG = 400
        self.qty = quantity
        self.COL = 64
        self.ROW = 0
        self.DESC = self.set_desc(
            "Fireballs are fired from the fingertips of the caster, striking each target in the area of "
            "effect - friend and foe alike.")
        # Spice


class Immolation(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Immolation"
        self.RAW = 'imo'
        self.SRT = 150
        self.SCL = SchoolType.elm
        self.MIN = 4
        self.UPG = 160
        self.qty = quantity
        self.COL = 0
        self.ROW = 0
        self.DESC = self.set_desc(
            "Fires a burst of flame at the target, who catches fire and takes 1-6 "
            "points of damage per round thereafter until the spell expires.")
        # Spice


class RemovePoison(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Remove Poison"
        self.RAW = 'rem_psn'
        self.SRT = 160
        self.SCL = SchoolType.elm
        self.MIN = 2
        self.UPG = 80
        self.qty = quantity
        self.COL = 192
        self.ROW = 128
        self.DESC = self.set_desc("Text")


class Strength(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Strength"
        self.RAW = 'str'
        self.SRT = 170
        self.SCL = SchoolType.elm
        self.MIN = 1
        self.UPG = 160
        self.qty = quantity
        self.COL = 0
        self.ROW = 192
        self.DESC = self.set_desc(
            "Target gains 2 Strength for each Rank of the spell. May only be cast once on each target.")
        # "Requires: Herb"


class Wind(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Wind"
        self.RAW = 'wnd'
        self.SRT = 180
        self.SCL = SchoolType.elm
        self.MIN = 2
        self.UPG = 520
        self.qty = quantity
        self.COL = 352
        self.ROW = 32
        self.DESC = self.set_desc(
            "The caster creates a vicious blast of wind which will attack one target, and dispels any "
            "fog that may be present on the battlefield.")
        # Herb


# Naming ###############################################################################################################
class Banishing(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Banishing"
        self.RAW = 'ban'
        self.SRT = 210
        self.SCL = SchoolType.nmg
        self.MIN = 4
        self.UPG = 520
        self.qty = quantity
        self.COL = 64
        self.ROW = 32
        self.DESC = self.set_desc("Text")


class Endurance(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Endurance"
        self.RAW = 'edu'
        self.SRT = 220
        self.SCL = SchoolType.nmg
        self.MIN = 2
        self.UPG = 320
        self.qty = quantity
        self.COL = 160
        self.ROW = 192
        self.DESC = self.set_desc(
            "Target gains 2 Endurance for each Rank of the spell. May only be cast once on each target.")
        # "Requires: Spice"


class SenseAura(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Sense Aura"
        self.RAW = 'sen_aur'
        self.SRT = 230
        self.SCL = SchoolType.nmg
        self.MIN = 3
        self.UPG = 400
        self.qty = quantity
        self.COL = 0
        self.ROW = 32
        self.DESC = self.set_desc(
            "Reveals a variety of information about the target: the higher the caster's rank in Sense Aura, "
            "the more information is revealed. May only be cast once on each target.")
        # "Requires: Herb"


class Teleportation(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Teleportation"
        self.RAW = 'tlp'
        self.SRT = 240
        self.SCL = SchoolType.nmg
        self.MIN = 8
        self.UPG = 320
        self.qty = quantity
        self.COL = 96
        self.ROW = 32
        self.DESC = self.set_desc("Caster teleports to a chosen point on the battlefield.")
        # "Requires: Gemstone"


class Weakness(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Weakness"
        self.RAW = 'wks'
        self.SRT = 250
        self.SCL = SchoolType.nmg
        self.MIN = 2
        self.UPG = 320
        self.qty = quantity
        self.COL = 32
        self.ROW = 32
        self.DESC = self.set_desc(
            "Target loses 2 Endurance for each Rank of the spell. May only be cast once on each target.")
        # "Requires: Herb"


# Star #################################################################################################################
class FrozenDoom(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Frozen Doom"
        self.RAW = 'frz_dom'
        self.SRT = 310
        self.SCL = SchoolType.str
        self.MIN = 6
        self.UPG = 600
        self.qty = quantity
        self.COL = 320
        self.ROW = 96
        self.DESC = self.set_desc("The target of this spell is frozen solid for the duration of the spell. "
                                  "Only affects targets of human size or smaller.")
        # Herb


class SolarWrath(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Solar Wrath"
        self.RAW = 'sol_wrt'
        self.SRT = 320
        self.SCL = SchoolType.str
        self.MIN = 4
        self.UPG = 80
        self.qty = quantity
        self.COL = 256
        self.ROW = 128
        self.DESC = self.set_desc("Text")


class StellarGravity(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Stellar Gravity"
        self.RAW = 'stl_gty'
        self.SRT = 330
        self.SCL = SchoolType.str
        self.MIN = 2
        self.UPG = 320
        self.qty = quantity
        self.COL = 224
        self.ROW = 128
        self.DESC = self.set_desc("Text")


class WebOfStarlight(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Web of Starlight"
        self.RAW = 'wos'
        self.SRT = 340
        self.SCL = SchoolType.str
        self.MIN = 3
        self.UPG = 400
        self.qty = quantity
        self.COL = 96
        self.ROW = 96
        self.DESC = self.set_desc("Target is encased in a web of energy that causes damage each round. "
                                  "Depending on their Strength, there is a chance that they may break out of the web. "
                                  "Only affects targets of human size or smaller.")
        # Gemstone


class Whitefire(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = "Whitefire"
        self.RAW = 'wfi'
        self.SRT = 350
        self.SCL = SchoolType.str
        self.MIN = 6
        self.UPG = 600
        self.qty = quantity
        self.COL = 128
        self.ROW = 96
        self.DESC = self.set_desc("Any single target within range is flash-fried by white fire.")
        # Spice
