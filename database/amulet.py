
"""
class: AmuletDatabase
"""

import enum

from constants import EquipmentType

# todo, alle amuletten afmaken


SPRITEPATH = 'resources/sprites/icons/equipment/amulet1.png'


class AmuletDatabase(enum.Enum):
    """..."""
    testamulet = dict(nam="Test Amulet",    srt=1, val=100, shp=True, wht=1, prt=1, col=0, row=0)
    testamulet2 = dict(nam="Test Amulet 2", srt=2, val=200, shp=True, wht=2, prt=2, col=0, row=0)


for amu in AmuletDatabase:
    amu.value['typ'] = EquipmentType.amu
    amu.value['spr'] = SPRITEPATH
