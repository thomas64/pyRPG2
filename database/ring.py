
"""
class: RingDatabase
"""

import enum

from constants import EquipmentType


SPRITEPATH = 'resources/sprites/icons/equipment/ring1.png'


class RingDatabase(enum.Enum):
    """..."""
    silverring = dict(nam="Regular Silver Ring",    srt=1,  val=1, shp=True,                     col=0,   row=0)
    goldring = dict(nam="Regular Gold Ring",        srt=2,  val=2, shp=True,                     col=32,  row=0)
    # todo, spell battery +20
    witchring = dict(nam="Witch Ring",              srt=3,  val=8, shp=False, min_int=25, wiz=2, col=0,  row=32)
    ringofhealing = dict(nam="Ring of Healing",     srt=4,  val=8, shp=False,             edu=5, col=32, row=32)
    etherialring = dict(nam="Etherial Ring",        srt=5,  val=8, shp=False,             prt=5, col=64, row=32)
    namersring = dict(nam="Namer's Ring",           srt=6,  val=8, shp=False,                    col=96, row=32)

for rng in RingDatabase:
    rng.value['typ'] = EquipmentType.rng
    rng.value['spr'] = SPRITEPATH
    rng.value['wht'] = 0
