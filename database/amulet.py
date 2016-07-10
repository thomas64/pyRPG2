
"""
class: AmuletDatabase
"""

import enum

from constants import EquipmentType


SPRITEPATH = 'resources/sprites/icons/equipment/amulet1.png'


class AmuletDatabase(enum.Enum):
    """..."""
    silvernecklace = dict(nam="Regular Silver Necklace", srt=1, val=1, shp=True,                      col=0,  row=0)
    goldnecklace = dict(nam="Regular Gold Necklace",     srt=2, val=2, shp=True,                      col=32, row=0)

    # todo, spell battery +25
    magesamulet = dict(nam="Mages Amulet",               srt=3, val=8, shp=False, min_int=26,         col=0,  row=32)
    shieldamulet = dict(nam="Shield Amulet",             srt=4, val=8, shp=False, min_wil=22, prt=10, col=32, row=32)

for amu in AmuletDatabase:
    amu.value['typ'] = EquipmentType.amu
    amu.value['spr'] = SPRITEPATH
    amu.value['wht'] = 0
