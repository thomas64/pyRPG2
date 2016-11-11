
"""
class: PouchItemDatabase
"""

import enum
import os

from constants import EquipmentType


POUCHPATH = "resources/sprites/icons/pouch"

GOLDIMG = os.path.join(POUCHPATH, "gold.png")
HERBIMG = os.path.join(POUCHPATH, "herbs.png")
SPICEIMG = os.path.join(POUCHPATH, "spices.png")
GEMSTONEIMG = os.path.join(POUCHPATH, "gemstones.png")
PHEALINGIMG = os.path.join(POUCHPATH, "p_healing.png")
NOTEPIMG = os.path.join(POUCHPATH, "note.png")


class PouchItemDatabase(enum.Enum):
    """..."""
    gold = dict(nam="Gold",                         srt=1,  spr=GOLDIMG,                desc="")

    herbs = dict(nam="Herbs",                       srt=2,  spr=HERBIMG,        val=1,  desc="")
    spices = dict(nam="Spices",                     srt=3,  spr=SPICEIMG,               desc="")
    gemstones = dict(nam="Gemstones",               srt=4,  spr=GEMSTONEIMG,            desc="")

    healing_potions = dict(nam="Healing Potion",    srt=5,  spr=PHEALINGIMG,    val=2,
                           desc="Restores some of the drinker's lost Endurance and Stamina. Creating a "
                                "Healing Potion requires 3 Herbs and an Alchemist rank of at least 1.")

    proofnote = dict(nam="Proofnote",               srt=10, spr=NOTEPIMG,               desc="")

    # todo, methods hier definieren voor de potions hun werkingen.

for itm in PouchItemDatabase:
    itm.value['typ'] = EquipmentType.itm
