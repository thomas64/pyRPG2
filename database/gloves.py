
"""
Gloves
"""

import collections

from constants import EquipmentType


# todo, alle handschoenen afmaken

SPRITEPATH = 'resources/sprites/icons/equipment/gloves1.png'

glv = collections.OrderedDict()

glv['leathergloves'] = dict(nam="Leather Gloves", srt=1, val=100, shp=True, wht=1, prt=1, col=0, row=0)
glv['testgloves2'] = dict(nam="Test Gloves 2",    srt=2, val=200, shp=True, wht=2, prt=2, col=0, row=0)

for value in glv.values():
    value['typ'] = EquipmentType.glv
    value['spr'] = SPRITEPATH
