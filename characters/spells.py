
"""
class: Spell
"""

from constants import SchoolType
from constants import SpellType


SPRITEPATH = 'resources/sprites/icons/spells/spells.png'
SPRITEPATH2 = 'resources/sprites/icons/spells/spells2.png'


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
        self.DESC = None

    def xp_cost(self):
        """
        ...
        :return:
        """
        # todo, lagere xp kosten zoals bij level.
        return int(self.UPG * ((self.qty + 1)**2))
        # todo, loremaster skill gebruiken voor 'korting'
        # oude uit vb:
        # return self.UPG * (self.qty ^ 2 + 2 * self.qty + 1)
        # - (((self.UPG * (self.qty ^ 2 + 2 * self.qty + 1)) / 100) * p(hc).lor3)

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

    def show_info(self):
        """
        ...
        :return:
        """
        return self.DESC


# Neutral ##############################################################################################################
class DispelNaming(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.dis_nmg.value
        self.RAW = SpellType.dis_nmg.name
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
        self.NAM = SpellType.dis_ncy.value
        self.RAW = SpellType.dis_ncy.name
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
        self.NAM = SpellType.dis_str.value
        self.RAW = SpellType.dis_str.name
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
        self.NAM = SpellType.mir.value
        self.RAW = SpellType.mir.name
        self.SRT = 40
        self.SCL = SchoolType.ntl
        self.MIN = 6
        self.UPG = 200
        self.qty = quantity
        self.COL = 352
        self.ROW = 96
        self.DESC = self.set_desc("Creates a shield that provides total resistance against the next "
                                  "incoming attack spells.")
        # Gemstone


class VsElemental(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.vs_elm.value
        self.RAW = SpellType.vs_elm.name
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
        self.NAM = SpellType.vs_nmg.value
        self.RAW = SpellType.vs_nmg.name
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
        self.NAM = SpellType.vs_ncy.value
        self.RAW = SpellType.vs_ncy.name
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
        self.NAM = SpellType.vs_str.value
        self.RAW = SpellType.vs_str.name
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
        self.NAM = SpellType.air_sld.value
        self.RAW = SpellType.air_sld.name
        self.SRT = 110
        self.SCL = SchoolType.elm
        self.MIN = 1
        self.UPG = 320
        self.qty = quantity
        self.COL = 352
        self.ROW = 128
        self.DESC = self.set_desc("All friendly entities within the range of the spell add 1 per Rank to "
                                  "their Protection value.")
        # "Requires: Gemstone"


class Debilitation(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.deb.value
        self.RAW = SpellType.deb.name
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
        self.NAM = SpellType.drg_flm.value
        self.RAW = SpellType.drg_flm.name
        self.SRT = 130
        self.SCL = SchoolType.elm
        self.MIN = 2
        self.UPG = 520
        self.qty = quantity
        self.COL = 32
        self.ROW = 0
        self.DESC = self.set_desc("The target(s) of this spell are attacked by wicked dragon flames "
                                  "emanating from the caster.")
        # Gemstone


class Fireball(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.frb.value
        self.RAW = SpellType.frb.name
        self.SRT = 140
        self.SCL = SchoolType.elm
        self.MIN = 5
        self.UPG = 400
        self.qty = quantity
        self.COL = 64
        self.ROW = 0
        self.DESC = self.set_desc("Fireballs are fired from the fingertips of the caster, striking each target in "
                                  "the area of effect - friend and foe alike.")
        # Spice


class Immolation(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.imo.value
        self.RAW = SpellType.imo.name
        self.SRT = 150
        self.SCL = SchoolType.elm
        self.MIN = 4
        self.UPG = 160
        self.qty = quantity
        self.COL = 0
        self.ROW = 0
        self.DESC = self.set_desc("Fires a burst of flame at the target, who catches fire and takes 1-6 "
                                  "points of damage per round thereafter until the spell expires.")
        # Spice


class RemovePoison(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.rem_psn.value
        self.RAW = SpellType.rem_psn.name
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
        self.NAM = SpellType.str.value
        self.RAW = SpellType.str.name
        self.SRT = 170
        self.SCL = SchoolType.elm
        self.MIN = 1
        self.UPG = 160
        self.qty = quantity
        self.COL = 0
        self.ROW = 192
        self.DESC = self.set_desc("Target gains 2 Strength for each Rank of the spell. "
                                  "May only be cast once on each target.")
        # "Requires: Herb"


class Wind(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.wnd.value
        self.RAW = SpellType.wnd.name
        self.SRT = 180
        self.SCL = SchoolType.elm
        self.MIN = 2
        self.UPG = 520
        self.qty = quantity
        self.COL = 352
        self.ROW = 32
        self.DESC = self.set_desc("The caster creates a vicious blast of wind which will attack one target, and "
                                  "dispels any fog that may be present on the battlefield.")
        # Herb


# Naming ###############################################################################################################
class Banishing(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.ban.value
        self.RAW = SpellType.ban.name
        self.SRT = 210
        self.SCL = SchoolType.nmg
        self.MIN = 4
        self.UPG = 520
        self.qty = quantity
        self.COL = 64
        self.ROW = 32
        self.DESC = self.set_desc("Any single elemental within range is banished from this plane of existence.")
        # Gemstone


class Endurance(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.edu.value
        self.RAW = SpellType.edu.name
        self.SRT = 220
        self.SCL = SchoolType.nmg
        self.MIN = 2
        self.UPG = 320
        self.qty = quantity
        self.COL = 160
        self.ROW = 192
        self.DESC = self.set_desc("Target gains 2 Endurance for each Rank of the spell. May only be cast "
                                  "once on each target.")
        # "Requires: Spice"


class SenseAura(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.sen_aur.value
        self.RAW = SpellType.sen_aur.name
        self.SRT = 230
        self.SCL = SchoolType.nmg
        self.MIN = 3
        self.UPG = 400
        self.qty = quantity
        self.COL = 0
        self.ROW = 32
        self.DESC = self.set_desc("Reveals a variety of information about the target: the higher the caster's rank in "
                                  "Sense Aura, the more information is revealed. May only be cast once on each target.")
        # "Requires: Herb"


class Teleportation(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.tlp.value
        self.RAW = SpellType.tlp.name
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
        self.NAM = SpellType.wks.value
        self.RAW = SpellType.wks.name
        self.SRT = 250
        self.SCL = SchoolType.nmg
        self.MIN = 2
        self.UPG = 320
        self.qty = quantity
        self.COL = 32
        self.ROW = 32
        self.DESC = self.set_desc("Target loses 2 Endurance for each Rank of the spell. May only be cast once "
                                  "on each target.")
        # "Requires: Herb"


# Star #################################################################################################################
class FrozenDoom(Spell):
    """..."""
    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.frz_dom.value
        self.RAW = SpellType.frz_dom.name
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
        self.NAM = SpellType.sol_wrt.value
        self.RAW = SpellType.sol_wrt.name
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
        self.NAM = SpellType.stl_gty.value
        self.RAW = SpellType.stl_gty.name
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
        self.NAM = SpellType.wos.value
        self.RAW = SpellType.wos.name
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
        self.NAM = SpellType.wfi.value
        self.RAW = SpellType.wfi.name
        self.SRT = 350
        self.SCL = SchoolType.str
        self.MIN = 6
        self.UPG = 600
        self.qty = quantity
        self.COL = 128
        self.ROW = 96
        self.DESC = self.set_desc("Any single target within range is flash-fried by white fire.")
        # Spice


# Necromancy ###########################################################################################################
class ControlZombies(Spell):
    """..."""
    ICON = SPRITEPATH2

    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.ctr_zom.value
        self.RAW = SpellType.ctr_zom.name
        self.SRT = 410
        self.SCL = SchoolType.ncy
        self.MIN = 3
        self.UPG = 400
        self.qty = quantity
        self.COL = 160
        self.ROW = 32
        self.DESC = self.set_desc("All targets within range of this spell have their movement rate increased by 2 per "
                                  "Rank. May only be cast once on each target.")
        # Herb


class Haste(Spell):
    """..."""
    ICON = SPRITEPATH2

    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.hst.value
        self.RAW = SpellType.hst.name
        self.SRT = 420
        self.SCL = SchoolType.ncy
        self.MIN = 4
        self.UPG = 520
        self.qty = quantity
        self.COL = 96
        self.ROW = 192
        self.DESC = self.set_desc("All targets within range of this spell have their movement rate increased by 2 per "
                                  "Rank. May only be cast once on each target.")
        # Spice


class WallOfBones(Spell):
    """..."""
    ICON = SPRITEPATH2

    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.wob.value
        self.RAW = SpellType.wob.name
        self.SRT = 430
        self.SCL = SchoolType.ncy
        self.MIN = 5
        self.UPG = 520
        self.qty = quantity
        self.COL = 224
        self.ROW = 0
        self.DESC = self.set_desc("Target is completely immobilized by a wall of bones.")
        # Herb


class SpiritShield(Spell):
    """..."""
    ICON = SPRITEPATH2

    def __init__(self, quantity):
        super().__init__()
        self.NAM = SpellType.spr_sld.value
        self.RAW = SpellType.spr_sld.name
        self.SRT = 440
        self.SCL = SchoolType.ncy
        self.MIN = 3
        self.UPG = 400
        self.qty = quantity
        self.COL = 352
        self.ROW = 128
        self.DESC = self.set_desc("All friendly entities within the range of the spell add 1 per Rank to their "
                                  "Protection value.")
        # Gemstone
