
"""
Amulet
"""

import collections

from . import EquipmentType

# todo, alle amuletten afmaken


SPRITEPATH = 'resources/sprites/icons/equipment/amulet1.png'

amu = collections.OrderedDict()

amu['testamulet'] = dict(nam="Test Amulet",    srt=1, val=100, shp=True, wht=1, prt=1, col=0, row=0)
amu['testamulet2'] = dict(nam="Test Amulet 2", srt=2, val=200, shp=True, wht=2, prt=2, col=0, row=0)

for value in amu.values():
    value['typ'] = EquipmentType.amu
    value['spr'] = SPRITEPATH
