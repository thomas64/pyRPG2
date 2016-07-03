
"""
class: BeltDatabase
"""

import enum

from constants import EquipmentType
from constants import ItemMaterial


# todo, alle gordels afmaken

SPRITEPATH = 'resources/sprites/icons/equipment/belt1.png'


class BeltDatabase(enum.Enum):
    """..."""
    #                                             val=prt**2+3
    leatherbelt = dict(nam="Leather Belt", srt=1, val=4, shp=True, wht=1, prt=1, col=0, row=0, mtr=ItemMaterial.ltr)
    testbelt2 = dict(nam="Test Belt 2",    srt=2, val=7, shp=True, wht=2, prt=2, col=0, row=0, mtr=ItemMaterial.ltr)


for blt in BeltDatabase:
    blt.value['typ'] = EquipmentType.blt
    blt.value['spr'] = SPRITEPATH
