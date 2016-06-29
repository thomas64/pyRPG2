
"""
class: BraceletDatabase
"""

import enum

from constants import EquipmentType


# todo, alle armbanden afmaken

SPRITEPATH = 'resources/sprites/icons/equipment/bracelet1.png'


class BraceletDatabase(enum.Enum):
    """..."""
    testbracelet = dict(nam="Test Bracelet",    srt=1, val=100, shp=True, wht=1, prt=1, col=0, row=0)
    testbracelet2 = dict(nam="Test Bracelet 2", srt=2, val=200, shp=True, wht=2, prt=2, col=0, row=0)


for brc in BraceletDatabase:
    brc.value['typ'] = EquipmentType.brc
    brc.value['spr'] = SPRITEPATH
