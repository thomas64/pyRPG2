
"""
class: GlovesDatabase
"""

import enum

from constants import EquipmentType
from constants import ItemMaterial


# todo, alle handschoenen afmaken

SPRITEPATH = 'resources/sprites/icons/equipment/gloves1.png'


class GlovesDatabase(enum.Enum):
    """..."""
    #                                                 val=prt**2+5
    leathergloves = dict(nam="Leather Gloves", srt=1, val=6, shp=True, wht=1, prt=1, col=0, row=0, mtr=ItemMaterial.ltr)
    testgloves2 = dict(nam="Test Gloves 2",    srt=2, val=9, shp=True, wht=2, prt=2, col=0, row=0, mtr=ItemMaterial.ltr)


for glv in GlovesDatabase:
    glv.value['typ'] = EquipmentType.glv
    glv.value['spr'] = SPRITEPATH
