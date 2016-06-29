
"""
class: GlovesDatabase
"""

import enum

from constants import EquipmentType


# todo, alle handschoenen afmaken

SPRITEPATH = 'resources/sprites/icons/equipment/gloves1.png'


class GlovesDatabase(enum.Enum):
    """..."""
    leathergloves = dict(nam="Leather Gloves", srt=1, val=100, shp=True, wht=1, prt=1, col=0, row=0)
    testgloves2 = dict(nam="Test Gloves 2",    srt=2, val=200, shp=True, wht=2, prt=2, col=0, row=0)


for glv in GlovesDatabase:
    glv.value['typ'] = EquipmentType.glv
    glv.value['spr'] = SPRITEPATH
