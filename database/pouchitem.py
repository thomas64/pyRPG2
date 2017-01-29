
"""
class: PouchItemDatabase
"""

import enum
import os

from constants import EquipmentType


POUCHPATH = 'resources/sprites/icons/pouch'
IMGPATH = 'resources/images/'

GOLDIMG = os.path.join(POUCHPATH, "gold.png")
HERBIMG = os.path.join(POUCHPATH, "herbs.png")
SPICEIMG = os.path.join(POUCHPATH, "spices.png")
GEMSTONEIMG = os.path.join(POUCHPATH, "gemstones.png")
CLOTHIMG = os.path.join(POUCHPATH, "cloth.png")
LEATHERIMG = os.path.join(POUCHPATH, "leather.png")
WOODIMG = os.path.join(POUCHPATH, "wood.png")
METALIMG = os.path.join(POUCHPATH, "metals.png")
POTIONBLUE = os.path.join(POUCHPATH, "potion_blue.png")
POTIONGREEN = os.path.join(POUCHPATH, "potion_green.png")
POTIONPURPLE = os.path.join(POUCHPATH, "potion_purple.png")
POTIONRED = os.path.join(POUCHPATH, "potion_red.png")
POTIONWHITE = os.path.join(POUCHPATH, "potion_white.png")
POTIONYELLOW = os.path.join(POUCHPATH, "potion_yellow.png")

NOTEPIMG = os.path.join(POUCHPATH, "note.png")


class PouchItemDatabase(enum.Enum):
    """..."""
    gold = dict(nam="Gold",           srt=1,  spr=GOLDIMG,
                desc="Gold can be used to pay for goods or services.")
    herbs = dict(nam="Herbs",         srt=2,  spr=HERBIMG,        val=1,
                 desc="Herbs are used in magical spells (Wizard Skill) and in creating potions (Alchemist Skill). "
                      "They also contain healing possibilities (Healer Skill).")
    spices = dict(nam="Spices",       srt=3,  spr=SPICEIMG,       val=1,
                  desc="Spices are used in magical spells (Wizard Skill) and in creating potions (Alchemist Skill).")
    gemstones = dict(nam="Gemstones", srt=4,  spr=GEMSTONEIMG,    val=1,
                     desc="Gemstones are used in magical spells (Wizard Skill) "
                          "and in creating potions (Alchemist Skill).")
    cloth = dict(nam="Cloth",         srt=5,  spr=CLOTHIMG,       val=1,
                 desc="Cloth is used for improving weapons, shields, armor and other equipment (Mechanic Skill).")
    leather = dict(nam="Leather",     srt=6,  spr=LEATHERIMG,     val=1,
                   desc="Leather is used for improving weapons, shields, armor and other equipment (Mechanic Skill).")
    wood = dict(nam="Wood",           srt=7,  spr=WOODIMG,        val=1,
                desc="Wood is used for improving weapons, shields, armor and other equipment (Mechanic Skill).")
    metals = dict(nam="Metals",       srt=8,  spr=METALIMG,       val=1,
                  desc="Metals are used for improving weapons, shields, armor and other equipment (Mechanic Skill).")

    proofnote = dict(nam="Proofnote", srt=40, spr=NOTEPIMG,       click=IMGPATH+'landkaart.jpg',
                     desc="A written note that says that you are not a monster.")  # todo, deze click is temp en voorb.

    hlg_pot = dict(nam="Healing Potion",      srt=15, spr=POTIONBLUE,    val=4,  hrb=3, spc=0, gms=0, alc=1, hp=5,
                   desc="Restores a fifth of the drinker's lost Endurance and Stamina. Creating a "
                        "Healing Potion requires 3 Herbs and an Alchemist rank of at least 1.")
    cur_pot = dict(nam="Curing Potion",       srt=16, spr=POTIONBLUE,    val=8,  hrb=3, spc=2, gms=0, alc=3, hp=3,
                   desc="A more powerful version of the Healing Potion, restores a third of the "
                        "drinker's lost Endurance and Stamina. Creating a "
                        "Curing Potion requires 3 Herbs, 2 Spices and an Alchemist rank of at least 3.")
    sta_pot = dict(nam="Stamina Potion",      srt=17, spr=POTIONWHITE,   val=11, hrb=4, spc=2, gms=0, alc=5,
                   desc="Restores all Stamina to the drinker. Creating a "
                        "Stamina Potion requires 4 Herbs, 2 Spices and an Alchemist rank of at least 5.")
    res_pot = dict(nam="Restore Potion",      srt=18, spr=POTIONWHITE,   val=15, hrb=5, spc=3, gms=0, alc=7,
                   desc="Restores full health to the drinker. Creating a "
                        "Restore Potion requires 5 Herbs, 3 Spices and an Alchemist rank of at least 7.")

    fir_flk = dict(nam="Fire Flask",          srt=19,  spr=POTIONRED,    val=4,  hrb=0, spc=1, gms=2, alc=1,
                   desc="A sticky, incendiary liquid that bursts into flame on contact with air. Creating a "
                        "Fire Flask requires 1 Spice, 2 Gemstones and an Alchemist rank of at least 1.")
    inf_flk = dict(nam="Inferno Flask",       srt=20, spr=POTIONRED,    val=9,  hrb=0, spc=3, gms=3, alc=3,
                   desc="A more powerful version of the Fire Flask. A sticky, incendiary liquid that bursts "
                        "into flame on contact with air. Creating an "
                        "Inferno Flask requires 3 Spices, 3 Gemstones and an Alchemist rank of at least 3.")
    acd_flk = dict(nam="Acid Flask",          srt=21, spr=POTIONGREEN,  val=10, hrb=0, spc=2, gms=3, alc=5,
                   desc="This vicious fluid eats into the flesh of any creature it touches, doing continuous damage. "
                        "Creating an "
                        "Acid Flask requires 2 Spices, 3 Gemstones and an Alchemist rank of at least 5.")
    slp_flk = dict(nam="Sleep Gas Flask",     srt=22, spr=POTIONGREEN,  val=13, hrb=3, spc=0, gms=3, alc=7,
                   desc="A liquid that vaporizes when exposed to air, forming a gas that drains the "
                        "mobility of those who breathe it. Creating a "
                        "Sleep Gas Flask requires 3 Herbs, 3 Gemstones and an Alchemist rank of at least 7.")

    ant_pot = dict(nam="Antidote Potion",     srt=23, spr=POTIONYELLOW, val=5,  hrb=1, spc=2, gms=0, alc=2,
                   desc="Halts the effects of poison, but does not restore damage already inflicted by poison. "
                        "Creating an "
                        "Antidote Potion requires 1 Herb, 2 Spices and an Alchemist rank of at least 2.")
    prt_pot = dict(nam="Protection Potion",   srt=24, spr=POTIONPURPLE, val=8,  hrb=2, spc=3, gms=1, alc=2,
                   desc="Temporarily increases the Protection of the drinker by 5 points during 1 battle. Creating a "
                        "Protection Potion requires 2 Herbs, 3 Spices, 1 Gemstone and an Alchemist rank of at least 2.")
    int_pot = dict(nam="Intelligence Potion", srt=25, spr=POTIONPURPLE, val=12, hrb=2, spc=1, gms=3, alc=6,
                   desc="Temporarily increases the Intelligence of the drinker by 5 points during 1 battle. Creating a "
                   "Intelligence Potion requires 2 Herbs, 1 Spice, 3 Gemstones and an Alchemist rank of at least 6.")
    wil_pot = dict(nam="Willpower Potion",    srt=26, spr=POTIONPURPLE, val=12, hrb=3, spc=2, gms=1, alc=6,
                   desc="Temporarily increases the Willpower of the drinker by 5 points during 1 battle. Creating a "
                        "Willpower Potion requires 3 Herbs, 2 Spices, 1 Gemstone and an Alchemist rank of at least 6.")
    dex_pot = dict(nam="Dexterity Potion",    srt=27, spr=POTIONPURPLE, val=12, hrb=1, spc=3, gms=2, alc=6,
                   desc="Temporarily increases the Dexterity of the drinker by 5 points during 1 battle. Creating a "
                        "Dexterity Potion requires 1 Herb, 3 Spices, 2 Gemstones and an Alchemist rank of at least 6.")
    agi_pot = dict(nam="Agility Potion",      srt=28, spr=POTIONPURPLE, val=12, hrb=3, spc=1, gms=2, alc=6,
                   desc="Temporarily increases the Agility of the drinker by 5 points during 1 battle. Creating a "
                        "Agility Potion requires 3 Herbs, 1 Spice, 2 Gemstones and an Alchemist rank of at least 6.")
    str_pot = dict(nam="Strength Potion",     srt=29, spr=POTIONPURPLE, val=12, hrb=1, spc=2, gms=3, alc=6,
                   desc="Temporarily increases the Strength of the drinker by 5 points during 1 battle. Creating a "
                        "Strength Potion requires 1 Herb, 2 Spices, 3 Gemstones and an Alchemist rank of at least 6.")
    stl_pot = dict(nam="Stealth Potion",      srt=30, spr=POTIONPURPLE, val=10, hrb=2, spc=2, gms=2, alc=4,
                   desc="Temporarily increases the Stealth rank of the drinker by 3 points during 1 battle. Creating a "
                        "Stealth Potion requires 2 Herbs, 2 Spices, 2 Gemstones and an Alchemist rank of at least 4.")

    # clarity_potion = dict(nam="Clarity Potion", srt=5, spr=REDPOTION, val=2,
    #                       desc="Temporarily improves the mental clarity of the character who drinks it, "
    #                            "assisting attempts to use the Loremaster skill. Creating a "
    #                            "Clarity Potion requires 3 Spices and an Alchemist rank of at least 3.")
    # charisma_potion = dict(nam="Charisma Potion", srt=5, spr=REDPOTION, val=2,
    #                        desc="Temporarily makes the drinker more charming and sociable, improving chances of "
    #                             "successfully using the Diplomacy skill. Creating a Charisma Potion "
    #                             "requires 1 Herb, 1 Gemstone, 2 Spices and an Alchemist rank of at least 2.")
    # defense_potion = dict(nam="Defense Potion", srt=5, spr=REDPOTION, val=2,
    #                       desc="Temporarily increases the defense (AP /armor protection) of the drinker, "
    #                            "reducing damage inflicted by opponents. Creating a "
    #                            "Defense Potion requires 2 Gemstones and an Alchemist rank of at least 2.")
    # restore_potion = dict(nam="Restore Potion", srt=5, spr=POTIONWHITE, val=2,
    #                       desc="In combat, this potion dispels the effects of Stupidity, Clumsiness, Debilitation, "
    #                            "Weakness, Exhaustion, and Wraith Touch. It has no effect out of combat. Creating a "
    #                            "Restore Potion requires 2 Gemstones, 2 Spices and an Alchemist rank of at least 3.")


for itm in PouchItemDatabase:
    itm.value['typ'] = EquipmentType.itm
